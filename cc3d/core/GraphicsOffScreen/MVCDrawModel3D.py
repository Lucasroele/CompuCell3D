from vtk.util.numpy_support import vtk_to_numpy
from .MVCDrawModelBase import MVCDrawModelBase
import vtk
import numpy as np
import math
from cc3d.core.GraphicsUtils.utils import extract_address_int_from_vtk_object, to_vtk_rgb
from cc3d.core.GraphicsOffScreen.MetadataHandler import MetadataHandler
from cc3d.cpp import PlayerPython
from cc3d.core.iterators import CellList, FocalPointPlasticityDataList, InternalFocalPointPlasticityDataList
from cc3d.cpp import CompuCell
import sys

VTK_MAJOR_VERSION = vtk.vtkVersion.GetVTKMajorVersion()
epsilon = sys.float_info.epsilon
MODULENAME = "------  MVCDrawModel3D.py"


class MVCDrawModel3D(MVCDrawModelBase):
    def __init__(self, boundary_strategy=None, ren=None):
        MVCDrawModelBase.__init__(self, boundary_strategy=boundary_strategy, ren=ren)

        self.initArea()
        self.setParams()

        self.usedDraw3DFlag = False

    # Sets up the VTK simulation area
    def initArea(self):
        # Zoom items
        self.zitems = []

        self.outlineDim = [0, 0, 0]

        self.numberOfTableColors = 1024
        self.scalarLUT = vtk.vtkLookupTable()
        self.scalarLUT.SetHueRange(0.67, 0.0)
        self.scalarLUT.SetSaturationRange(1.0, 1.0)
        self.scalarLUT.SetValueRange(1.0, 1.0)
        self.scalarLUT.SetAlphaRange(1.0, 1.0)
        self.scalarLUT.SetNumberOfColors(self.numberOfTableColors)
        self.scalarLUT.Build()

        self.lowTableValue = self.scalarLUT.GetTableValue(0)
        self.highTableValue = self.scalarLUT.GetTableValue(self.numberOfTableColors - 1)

        ## Set up the mapper and actor (3D) for concentration field.
        self.conMapper = vtk.vtkPolyDataMapper()
        # self.conActor = vtk.vtkActor()

        # self.glyphsActor=vtk.vtkActor()
        self.glyphsMapper = vtk.vtkPolyDataMapper()

        self.cellGlyphsMapper = vtk.vtkPolyDataMapper()
        self.FPPLinksMapper = vtk.vtkPolyDataMapper()

        # Weird attributes
        # self.typeActors             = {} # vtkActor
        self.smootherFilters = {}  # vtkSmoothPolyDataFilter
        self.polyDataNormals = {}  # vtkPolyDataNormals
        self.typeExtractors = {}  # vtkDiscreteMarchingCubes
        self.typeExtractorMappers = {}  # vtkPolyDataMapper

    def is_lattice_hex(self, drawing_params):
        """
        returns if flag that states if the lattice is hex or not. Notice
        In 2D we may use cartesian coordinates for certain projections
        :return: {bool}
        """
        lattice_type_str = self.get_lattice_type_str()
        if lattice_type_str.lower() == "hexagonal":
            return True
        else:
            return False

    def init_cell_field_actors_borderless(self, actor_specs, drawing_params=None):

        hex_flag = False
        lattice_type_str = self.get_lattice_type_str()
        if lattice_type_str.lower() == "hexagonal":
            hex_flag = True

        # todo 5 - check if this should be called earlier
        # self.extractCellFieldData() # initializes self.usedCellTypesList

        field_dim = self.currentDrawingParameters.bsd.fieldDim
        cell_type_image_data = vtk.vtkImageData()

        cell_type_image_data.SetDimensions(
            field_dim.x + 2, field_dim.y + 2, field_dim.z + 2
        )  # adding 1 pixel border around the lattice to make rendering smooth at lattice borders
        cell_type_image_data.GetPointData().SetScalars(self.cell_type_array)
        voi = vtk.vtkExtractVOI()

        if VTK_MAJOR_VERSION >= 6:
            voi.SetInputData(cell_type_image_data)
        else:
            voi.SetInput(cell_type_image_data)

        #        voi.SetVOI(1,self.dim[0]-1, 1,self.dim[1]-1, 1,self.dim[2]-1 )  # crop out the artificial boundary layer that we created
        voi.SetVOI(0, 249, 0, 189, 0, 170)

        # # todo 5- check if it is possible to call it once
        # self.usedCellTypesList = self.extractCellFieldData()

        number_of_actors = len(self.used_cell_types_list)

        # creating and initializing filters, smoothers and mappers - one for each cell type

        filterList = [vtk.vtkDiscreteMarchingCubes() for i in range(number_of_actors)]
        smootherList = [vtk.vtkSmoothPolyDataFilter() for i in range(number_of_actors)]
        normalsList = [vtk.vtkPolyDataNormals() for i in range(number_of_actors)]
        mapperList = [vtk.vtkPolyDataMapper() for i in range(number_of_actors)]

        # actorCounter=0
        # for i in usedCellTypesList:
        for actorCounter, actor_number in enumerate(self.used_cell_types_list):
            # for actorCounter in xrange(len(self.usedCellTypesList)):

            if VTK_MAJOR_VERSION >= 6:
                filterList[actorCounter].SetInputData(cell_type_image_data)
            else:
                filterList[actorCounter].SetInput(cell_type_image_data)

            #            filterList[actorCounter].SetInputConnection(voi.GetOutputPort())

            # filterList[actorCounter].SetValue(0, usedCellTypesList[actorCounter])
            filterList[actorCounter].SetValue(0, self.used_cell_types_list[actorCounter])
            smootherList[actorCounter].SetInputConnection(filterList[actorCounter].GetOutputPort())
            #            smootherList[actorCounter].SetNumberOfIterations(200)
            normalsList[actorCounter].SetInputConnection(smootherList[actorCounter].GetOutputPort())
            normalsList[actorCounter].SetFeatureAngle(45.0)
            mapperList[actorCounter].SetInputConnection(normalsList[actorCounter].GetOutputPort())
            mapperList[actorCounter].ScalarVisibilityOff()

            actors_dict = actor_specs.actors_dict

            cell_type_lut = self.get_type_lookup_table()
            cell_type_lut_max = cell_type_lut.GetNumberOfTableValues() - 1

            if actor_number in list(actors_dict.keys()):
                actor = actors_dict[actor_number]
                actor.SetMapper(mapperList[actorCounter])

                actor.GetProperty().SetDiffuseColor(
                    cell_type_lut.GetTableValue(self.used_cell_types_list[actorCounter])[0:3]
                )

                # actor.GetProperty().SetDiffuseColor(
                #     # self.celltypeLUT.GetTableValue(self.usedCellTypesList[actorCounter])[0:3])
                #     self.celltypeLUT.GetTableValue(actor_number)[0:3])
                if hex_flag:
                    actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)
                    # actor.GetProperty().SetOpacity(0.5)

    def init_cell_field_glyphs_actors(self, actor_specs, drawing_params=None):
        # using just one actor

        centroids = vtk.vtkPoints()
        volume_scaling_factors = vtk.vtkFloatArray()
        volume_scaling_factors.SetName("volume_scaling_factors")

        cell_types = vtk.vtkIntArray()
        cell_types.SetName("cell_types")
        centroids_addr = extract_address_int_from_vtk_object(vtkObj=centroids)
        cell_types_addr = extract_address_int_from_vtk_object(vtkObj=cell_types)
        volume_scaling_factors_addr = extract_address_int_from_vtk_object(vtkObj=volume_scaling_factors)

        types_invisible = PlayerPython.vectorint()
        for type_label in drawing_params.screenshot_data.invisible_types:
            types_invisible.append(int(type_label))

        used_types = self.field_extractor.fillCellFieldGlyphs3D(
            centroids_addr, volume_scaling_factors_addr, cell_types_addr, types_invisible
        )
        mapper = vtk.vtkPolyDataMapper()

        # polydata should be initialized/created AFTER all arrays have been filled in
        centroid_polydata = vtk.vtkPolyData()
        centroid_polydata.SetPoints(centroids)
        centroid_polydata.GetPointData().AddArray(volume_scaling_factors)
        centroid_polydata.GetPointData().AddArray(cell_types)

        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(1)

        try:
            actor = list(actor_specs.actors_dict.values())[0]
        except IndexError:
            print("Could not find any actor for listed cell types")
            return

        glyphs = vtk.vtkGlyph3D()

        glyphs.SetInputData(centroid_polydata)
        glyphs.SetSourceConnection(0, sphere.GetOutputPort())

        glyphs.ScalingOn()
        glyphs.SetScaleModeToScaleByScalar()
        glyphs.SetColorModeToColorByScalar()

        glyphs.SetScaleFactor(1)  # Overall scaling factor

        # Tell it to index into the glyph table according to scalars
        glyphs.SetIndexModeToScalar()

        # Tell glyph which attribute arrays to use for what
        # see also https://stackoverflow.com/questions/29768049/
        # python-vtk-glyphs-with-independent-position-orientation-color-and-height
        glyphs.SetInputArrayToProcess(0, 0, 0, 0, "volume_scaling_factors")  # 0 - scalars for scaling
        glyphs.SetInputArrayToProcess(3, 0, 0, 0, "cell_types")  # 3 - color

        cell_type_lut = self.get_type_lookup_table()
        mapper.SetInputConnection(glyphs.GetOutputPort())
        mapper.SetLookupTable(cell_type_lut)
        mapper.ScalarVisibilityOn()
        mapper.SetScalarRange(0, cell_type_lut.GetNumberOfTableValues() - 1)
        mapper.SetColorModeToMapScalars()

        actor.SetMapper(mapper)

        if self.is_lattice_hex(drawing_params=drawing_params):
            actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)

    def init_cell_field_glyphs_actors_py(self, actor_specs, drawing_params=None):
        # using just one actor

        from cc3d.core.PySteppables import CellList

        inventory = self.currentDrawingParameters.bsd.sim.getPotts().getCellInventory()
        cell_list = CellList(inventory)

        centroids = vtk.vtkPoints()
        volume_scaling_factors = vtk.vtkFloatArray()
        volume_scaling_factors.SetName("volume_scaling_factors")

        cell_types = vtk.vtkIntArray()
        cell_types.SetName("cell_types")

        mapper = vtk.vtkPolyDataMapper()

        used_cell_types_dict = {cell_type: 0 for cell_type in self.used_cell_types_list}

        # polydata should be initialized/created AFTER all arrays have been filled in
        centroid_polydata = vtk.vtkPolyData()
        centroid_polydata.SetPoints(centroids)
        centroid_polydata.GetPointData().AddArray(volume_scaling_factors)
        centroid_polydata.GetPointData().AddArray(cell_types)

        for cell in cell_list:
            cell_type = cell.type
            used_type = used_cell_types_dict.get(cell_type, None)
            if used_type is None:
                continue

            centroids.InsertNextPoint(cell.xCOM, cell.yCOM, cell.zCOM)
            # (3/(4*math.pi))**0.333 = 0.62
            volume_scaling_factors.InsertNextValue(0.62 * cell.volume**0.333)
            cell_types.InsertNextValue(cell_type)
            print(f"inserting cell type {cell.xCOM} {cell.yCOM} type= {cell_type}")

        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(1)
        # sphere.SetThetaResolution(2)  # increase these values for a higher-res sphere glyph
        # sphere.SetPhiResolution(2)

        try:
            actor = list(actor_specs.actors_dict.values())[0]
        except IndexError:
            print("Could not find any actor for listed cell types")
            return

        glyphs = vtk.vtkGlyph3D()

        glyphs.SetInputData(centroid_polydata)
        glyphs.SetSourceConnection(0, sphere.GetOutputPort())

        glyphs.ScalingOn()
        glyphs.SetScaleModeToScaleByScalar()
        glyphs.SetColorModeToColorByScalar()

        glyphs.SetScaleFactor(1)  # Overall scaling factor

        # Tell it to index into the glyph table according to scalars
        glyphs.SetIndexModeToScalar()

        # Tell glyph which attribute arrays to use for what
        # see also https://stackoverflow.com/questions/29768049/
        # python-vtk-glyphs-with-independent-position-orientation-color-and-height
        glyphs.SetInputArrayToProcess(0, 0, 0, 0, "volume_scaling_factors")  # 0 - scalars for scaling
        glyphs.SetInputArrayToProcess(3, 0, 0, 0, "cell_types")  # 3 - color

        cell_type_lut = self.get_type_lookup_table()
        mapper.SetInputConnection(glyphs.GetOutputPort())
        mapper.SetLookupTable(cell_type_lut)
        mapper.ScalarVisibilityOn()
        mapper.SetScalarRange(0, cell_type_lut.GetNumberOfTableValues() - 1)
        mapper.SetColorModeToMapScalars()
        # TODO add hex actor scaling
        actor.SetMapper(mapper)

    def init_cell_field_glyphs_actors_ok(self, actor_specs, drawing_params=None):

        # ss = vtk.vtkSphereSource()
        # ss.SetRadius(1.0)
        # # ss.SetThetaResolution(2)  # increase these values for a higher-res sphere glyph
        # # ss.SetPhiResolution(2)
        #
        #
        # centroid_polydata = vtk.vtkPolyData()
        #
        # centroids = vtk.vtkPoints()
        # centroids.InsertNextPoint(10, 10, 10)
        # centroids.InsertNextPoint(20, 20, 20)
        #
        # volume_scaling_factors = vtk.vtkFloatArray()
        # volume_scaling_factors.SetName('volume_scaling_factors')
        # volume_scaling_factors.InsertNextValue(5)
        # volume_scaling_factors.InsertNextValue(5)
        #
        # centroid_polydata.SetPoints(centroids)
        # centroid_polydata.GetPointData().AddArray(volume_scaling_factors)
        #
        # # Set up the glyph filter
        #
        # glyph = vtk.vtkGlyph3D()
        # # glyph.SetInputConnection(elev.GetOutputPort())
        # glyph.SetInputData(centroid_polydata)
        #
        # # Here is where we build the glyph table
        # # that will be indexed into according to the IndexMode
        # glyph.SetSourceConnection(0, ss.GetOutputPort())
        # # glyph.SetSourceConnection(0, ss.GetOutputPort())
        # # glyph.SetSourceConnection(1, cs.GetOutputPort())
        # # # glyph.SetSourceConnection(1, ss.GetOutputPort())
        # # glyph.SetSourceConnection(2, cs2.GetOutputPort())
        #
        # glyph.ScalingOn()
        # glyph.SetScaleModeToScaleByScalar()
        # # glyph.SetVectorModeToUseVector()
        # # glyph.OrientOn()
        # glyph.SetScaleFactor(1)  # Overall scaling factor
        # # glyph.SetRange(0, 1)  # Default is (0,1)
        #
        # # Tell it to index into the glyph table according to scalars
        # # glyph.SetIndexModeToScalar()
        #
        # # Tell glyph which attribute arrays to use for what
        # glyph.SetInputArrayToProcess(0, 0, 0, 0, 'volume_scaling_factors')  # scalars
        # # glyph.SetInputArrayToProcess(1, 0, 0, 0, 'RTDataGradient')  # vectors
        #
        # coloring_by = 'Elevation'
        # mapper = vtk.vtkPolyDataMapper()
        # mapper.SetInputConnection(glyph.GetOutputPort())
        # mapper.SetScalarModeToUsePointFieldData()
        # # mapper.SetColorModeToMapScalars()
        # # mapper.ScalarVisibilityOn()
        # actor_specs.actors_dict[1].SetMapper(mapper)
        # return

        from cc3d.core.PySteppables import CellList

        inventory = self.currentDrawingParameters.bsd.sim.getPotts().getCellInventory()
        cell_list = CellList(inventory)

        # centroidsPD = vtk.vtkPolyData()
        # centroidsPD.SetPoints(centroidPoints)
        # centroidsPD.GetPointData().SetScalars(cellTypes)
        #
        # #        if self.scaleGlyphsByVolume:
        # centroidsPD.GetPointData().AddArray(cellScalars)

        centroid_polydata_dict = {}
        centroid_dict = {}
        volume_scaling_factors_dict = {}
        mapper_dict = {}

        for actor_counter, cell_type in enumerate(self.used_cell_types_list):
            centroid_dict[cell_type] = vtk.vtkPoints()
            # centroid_dict[cell_type].SetName("centroids")
            volume_scaling_factors_dict[cell_type] = vtk.vtkFloatArray()
            volume_scaling_factors_dict[cell_type].SetName("volume_scaling_factors")
            mapper_dict[cell_type] = vtk.vtkPolyDataMapper()

        for cell in cell_list:
            cell_type = cell.type
            centroids = centroid_dict.get(cell_type, None)
            if centroids is None:
                continue
            volume_scaling_factors = volume_scaling_factors_dict[cell_type]

            centroids.InsertNextPoint(cell.xCOM, cell.yCOM, cell.zCOM)
            # (3/(4*math.pi))**0.333 = 0.62
            volume_scaling_factors.InsertNextValue(0.62 * cell.volume**0.333)

        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(1)
        # sphere.SetThetaResolution(2)  # increase these values for a higher-res sphere glyph
        # sphere.SetPhiResolution(2)

        glyphs_dict = {}
        centroid_polydata = {}
        for actor_counter, cell_type in enumerate(self.used_cell_types_list):
            centroids = centroid_dict[cell_type]
            volume_scaling_factors = volume_scaling_factors_dict[cell_type]

            centroid_polydata = vtk.vtkPolyData()
            centroid_polydata.SetPoints(centroids)
            centroid_polydata.GetPointData().AddArray(volume_scaling_factors)

            glyphs_dict[cell_type] = vtk.vtkGlyph3D()
            glyphs = glyphs_dict[cell_type]

            glyphs.SetInputData(centroid_polydata)
            glyphs.SetSourceConnection(sphere.GetOutputPort())

            glyphs.ScalingOn()
            glyphs.SetScaleModeToScaleByScalar()
            # glyph.SetVectorModeToUseVector()
            # glyph.OrientOn()
            glyphs.SetScaleFactor(1)  # Overall scaling factor

            # Tell glyph which attribute arrays to use for what
            glyphs.SetInputArrayToProcess(0, 0, 0, 0, "volume_scaling_factors")  # scalars
            # # Tell glyph which attribute arrays to use for what
            # glyphs.SetInputArrayToProcess(0, 0, 0, 0, 'volume_scaling_factors')
            # glyphs.SetIndexModeToScalar()
            # # overall magnification - scales all spheres in a given glyph3D
            # glyphs.SetScaleFactor(1.0)
            #
            #
            # glyphs.SetScaleModeToScaleByScalar()

            mapper = mapper_dict[cell_type]
            mapper.SetInputConnection(glyphs.GetOutputPort())
            # call to SetScalarModeToUsePointFieldData() is essential
            # if we want to color actors individually using  actor.GetProperty().SetDiffuseColor(...)

            mapper.SetScalarModeToUsePointFieldData()

            actor = actor_specs.actors_dict.get(cell_type, None)
            if actor is None:
                continue
            actor.SetMapper(mapper)

            cell_type_lut = self.get_type_lookup_table()

            actor.GetProperty().SetDiffuseColor(cell_type_lut.GetTableValue(cell_type)[0:3])
            # actor.GetProperty().SetDiffuseColor([1.0, 0, 0])

    def init_cell_field_borders_actors(self, actor_specs, drawing_params=None):
        """
        initializes cell field actors where each cell is rendered individually as a separate spatial domain
        :param actor_specs: {ActorSpecs}
        :param drawing_params: {DrawingParameters}
        :return: None
        """

        field_dim = self.currentDrawingParameters.bsd.fieldDim

        hex_flag = self.is_lattice_hex(drawing_params=drawing_params)

        cell_type_image_data = vtk.vtkImageData()

        # adding 1 pixel border around the lattice to make rendering smooth at lattice borders
        cell_type_image_data.SetDimensions(field_dim.x + 2, field_dim.y + 2, field_dim.z + 2)

        cell_type_image_data.GetPointData().SetScalars(self.cell_id_array)

        # create a different actor for each cell type
        number_of_actors = len(self.used_cell_types_list)

        # creating and initializing filters, smoothers and mappers - one for each cell type
        filter_list = [vtk.vtkDiscreteMarchingCubes() for i in range(number_of_actors)]
        smoother_list = [vtk.vtkSmoothPolyDataFilter() for i in range(number_of_actors)]
        normals_list = [vtk.vtkPolyDataNormals() for i in range(number_of_actors)]
        mapper_list = [vtk.vtkPolyDataMapper() for i in range(number_of_actors)]

        for actor_counter, actor_number in enumerate(self.used_cell_types_list):

            if VTK_MAJOR_VERSION >= 6:
                filter_list[actor_counter].SetInputData(cell_type_image_data)
            else:
                filter_list[actor_counter].SetInput(cell_type_image_data)

            if self.used_cell_types_list[actor_counter] >= 1:
                ct_all = vtk_to_numpy(self.cell_type_array)
                cid_all = vtk_to_numpy(self.cell_id_array)

                cid_unique = np.unique(cid_all[ct_all == actor_number])

                for idx in range(len(cid_unique)):
                    filter_list[actor_counter].SetValue(idx, cid_unique[idx])

            else:
                filter_list[actor_counter].SetValue(0, 13)  # rwh: what the??

            smoother_list[actor_counter].SetInputConnection(filter_list[actor_counter].GetOutputPort())
            normals_list[actor_counter].SetInputConnection(smoother_list[actor_counter].GetOutputPort())
            normals_list[actor_counter].SetFeatureAngle(45.0)
            mapper_list[actor_counter].SetInputConnection(normals_list[actor_counter].GetOutputPort())
            mapper_list[actor_counter].ScalarVisibilityOff()

            actors_dict = actor_specs.actors_dict
            if actor_number in list(actors_dict.keys()):
                actor = actors_dict[actor_number]
                actor.SetMapper(mapper_list[actor_counter])

                cell_type_lut = self.get_type_lookup_table()

                actor.GetProperty().SetDiffuseColor(cell_type_lut.GetTableValue(actor_number)[0:3])

                if hex_flag:
                    actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)

    # original rendering technique (and still used if Vis->Cell Borders not checked) - vkDiscreteMarchingCubes
    # on celltype
    def init_cell_field_actors(self, actor_specs, drawing_params=None):
        self.init_cell_field_glyphs_actors(actor_specs=actor_specs, drawing_params=drawing_params)
        return
        if drawing_params.screenshot_data.cell_borders_on:
            self.init_cell_field_borders_actors(actor_specs=actor_specs, drawing_params=drawing_params)
        else:
            self.init_cell_field_actors_borderless(actor_specs=actor_specs, drawing_params=drawing_params)

    def init_concentration_field_glyphs_actors(self, actor_specs, drawing_params=None):

        # from cc3d.core.PySteppables import CellList
        #
        # inventory = self.currentDrawingParameters.bsd.sim.getPotts().getCellInventory()
        # cell_list = CellList(inventory)

        centroids = vtk.vtkPoints()
        volume_scaling_factors = vtk.vtkFloatArray()
        volume_scaling_factors.SetName("volume_scaling_factors")

        scalar_value_at_com_array = vtk.vtkFloatArray()
        scalar_value_at_com_array.SetName("scalar_value_at_com")

        centroids_addr = extract_address_int_from_vtk_object(vtkObj=centroids)
        scalar_value_at_com_addr = extract_address_int_from_vtk_object(vtkObj=scalar_value_at_com_array)
        volume_scaling_factors_addr = extract_address_int_from_vtk_object(vtkObj=volume_scaling_factors)

        mapper = vtk.vtkPolyDataMapper()

        used_cell_types_dict = {cell_type: 0 for cell_type in self.used_cell_types_list}

        # polydata should be initialized/created AFTER all arrays have been filled in
        centroid_polydata = vtk.vtkPolyData()
        centroid_polydata.SetPoints(centroids)
        centroid_polydata.GetPointData().AddArray(volume_scaling_factors)
        # centroid_polydata.GetPointData().AddArray(cell_types)
        centroid_polydata.GetPointData().AddArray(scalar_value_at_com_array)

        field_type = drawing_params.fieldType.lower()
        field_name = drawing_params.fieldName
        scene_metadata = drawing_params.screenshot_data.metadata
        mdata = MetadataHandler(mdata=scene_metadata)

        types_invisible = PlayerPython.vectorint()
        for type_label in drawing_params.screenshot_data.invisible_types:
            types_invisible.append(int(type_label))

        if field_type == "confield":
            used_cell_types = self.field_extractor.fillConFieldGlyphs3D(
                field_name, centroids_addr, volume_scaling_factors_addr, scalar_value_at_com_addr, types_invisible
            )
        elif field_type == "scalarfield":
            used_cell_types = self.field_extractor.fillScalarFieldGlyphs3D(
                field_name, centroids_addr, volume_scaling_factors_addr, scalar_value_at_com_addr, types_invisible
            )
        elif field_type == "scalarfieldcelllevel":
            used_cell_types = self.field_extractor.fillScalarFieldCellLevelGlyphs3D(
                field_name, centroids_addr, volume_scaling_factors_addr, scalar_value_at_com_addr, types_invisible
            )

        if not len(used_cell_types):
            return
        # if field_type == 'confield':
        #     return
        #     # fill_successful = self.field_extractor.fillConFieldData3D(con_array_int_addr, cell_type_con_int_addr,
        #     #                                                           field_name, types_invisible,
        #     #                                                           use_cell_type_thresholding)
        # elif field_type == 'scalarfield':
        #     fill_successful = self.field_extractor.fillScalarFieldGlyphs3D(field_name, con_array_int_addr, cell_type_con_int_addr,
        #                                                                  , types_invisible,
        #                                                                  use_cell_type_thresholding)
        # elif field_type == 'scalarfieldcelllevel':
        #     return
        #     # fill_successful = self.field_extractor.fillScalarFieldCellLevelData3D(con_array_int_addr,
        #     #                                                                       cell_type_con_int_addr, field_name,
        #     #                                                                       types_invisible,
        #     #                                                                       use_cell_type_thresholding)
        #

        # for idx, cell in enumerate(cell_list):
        #     cell_type = cell.type
        #     used_type = used_cell_types_dict.get(cell_type, None)
        #     if used_type is None:
        #         continue
        #
        #     centroids.InsertNextPoint(cell.xCOM, cell.yCOM, cell.zCOM)
        #     # (3/(4*math.pi))**0.333 = 0.62
        #     volume_scaling_factors.InsertNextValue(0.62*cell.volume ** 0.333)
        #     cell_types.InsertNextValue(cell_type)
        #     scalar_value_at_com_array.InsertNextValue(idx)
        #     print(f'inserting cell type {cell.xCOM} {cell.yCOM} type= {cell_type}')

        sphere = vtk.vtkSphereSource()
        sphere.SetRadius(1)
        # sphere.SetThetaResolution(2)  # increase these values for a higher-res sphere glyph
        # sphere.SetPhiResolution(2)

        try:
            actor = list(actor_specs.actors_dict.values())[0]
        except IndexError:
            print("Could not find any actor for listed cell types")
            return

        glyphs = vtk.vtkGlyph3D()

        glyphs.SetInputData(centroid_polydata)
        glyphs.SetSourceConnection(0, sphere.GetOutputPort())

        glyphs.ScalingOn()
        glyphs.SetScaleModeToScaleByScalar()
        glyphs.SetColorModeToColorByScalar()

        glyphs.SetScaleFactor(1)  # Overall scaling factor

        # Tell it to index into the glyph table according to scalars
        glyphs.SetIndexModeToScalar()

        # Tell glyph which attribute arrays to use for what
        # see also https://stackoverflow.com/questions/29768049/
        # python-vtk-glyphs-with-independent-position-orientation-color-and-height
        glyphs.SetInputArrayToProcess(0, 0, 0, 0, "volume_scaling_factors")  # 0 - scalars for scaling
        # glyphs.SetInputArrayToProcess(3, 0, 0, 0, 'cell_types')  # 3 - color
        glyphs.SetInputArrayToProcess(3, 0, 0, 0, "scalar_value_at_com")  # 3 - color

        field_name = drawing_params.fieldName
        scene_metadata = drawing_params.screenshot_data.metadata

        range_array = scalar_value_at_com_array.GetRange()
        min_con = range_array[0]
        max_con = range_array[1]

        min_max_dict = self.get_min_max_metadata(scene_metadata=scene_metadata, field_name=field_name)
        min_range_fixed = min_max_dict["MinRangeFixed"]
        max_range_fixed = min_max_dict["MaxRangeFixed"]
        min_range = min_max_dict["MinRange"]
        max_range = min_max_dict["MaxRange"]

        # Note! should really avoid doing a getSetting with each step to speed up the rendering;
        # only update when changed in Prefs
        if min_range_fixed:
            min_con = min_range

        if max_range_fixed:
            max_con = max_range

        # cell_type_lut = self.get_type_lookup_table()
        lut = self.scalarLUT
        # self.conMapper.SetScalarRange(min_con, max_con)

        mapper.SetInputConnection(glyphs.GetOutputPort())
        # mapper.SetLookupTable(cell_type_lut)
        mapper.SetLookupTable(lut)
        mapper.ScalarVisibilityOn()
        mapper.SetScalarRange(min_con, max_con)
        # mapper.SetScalarRange(0, cell_type_lut.GetNumberOfTableValues() - 1)
        mapper.SetColorModeToMapScalars()

        actor.SetMapper(mapper)
        if self.is_lattice_hex(drawing_params=drawing_params):
            actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)

    def init_concentration_field_actors(self, actor_specs, drawing_params=None):
        """
        initializes concentration field actors
        :param actor_specs:
        :param drawing_params:
        :return: None
        """
        self.init_concentration_field_glyphs_actors(actor_specs=actor_specs, drawing_params=drawing_params)
        return

        actors_dict = actor_specs.actors_dict

        field_dim = self.currentDrawingParameters.bsd.fieldDim
        dim = [field_dim.x, field_dim.y, field_dim.z]
        field_name = drawing_params.fieldName
        scene_metadata = drawing_params.screenshot_data.metadata
        mdata = MetadataHandler(mdata=scene_metadata)

        try:
            isovalues = mdata.get("ScalarIsoValues", default=[])
            isovalues = list([float(x) for x in isovalues])
        except:
            print("Could not process isovalue list ")
            isovalues = []

        try:
            num_isos = mdata.get("NumberOfContourLines", default=3)
        except:
            print("could not process NumberOfContourLines setting")
            num_isos = 0

        try:
            show_contours = mdata.get("ContoursOn", default=False)
        except:
            print("could not process ContoursOn setting")
            show_contours = False

        hex_flag = False
        lattice_type_str = self.get_lattice_type_str()
        if lattice_type_str.lower() == "hexagonal":
            hex_flag = True

        types_invisible = PlayerPython.vectorint()
        for type_label in drawing_params.screenshot_data.invisible_types:
            types_invisible.append(int(type_label))

        # self.isovalStr = Configuration.getSetting("ScalarIsoValues", field_name)
        # if type(self.isovalStr) == QVariant:
        #     self.isovalStr = str(self.isovalStr.toString())
        # else:
        #     self.isovalStr = str(self.isovalStr)

        con_array = vtk.vtkDoubleArray()
        con_array.SetName("concentration")
        con_array_int_addr = extract_address_int_from_vtk_object(vtkObj=con_array)

        cell_type_con = vtk.vtkIntArray()
        cell_type_con.SetName("concelltype")
        cell_type_con_int_addr = extract_address_int_from_vtk_object(vtkObj=cell_type_con)

        field_type = drawing_params.fieldType.lower()
        # cell_type thresholding will return 0-1 array 0 for medium and 1 for all other visible types
        use_cell_type_thresholding = not show_contours

        fill_successful = False
        if field_type == "confield":
            fill_successful = self.field_extractor.fillConFieldData3D(
                con_array_int_addr, cell_type_con_int_addr, field_name, types_invisible, use_cell_type_thresholding
            )
        elif field_type == "scalarfield":
            fill_successful = self.field_extractor.fillScalarFieldData3D(
                con_array_int_addr, cell_type_con_int_addr, field_name, types_invisible, use_cell_type_thresholding
            )
        elif field_type == "scalarfieldcelllevel":
            fill_successful = self.field_extractor.fillScalarFieldCellLevelData3D(
                con_array_int_addr, cell_type_con_int_addr, field_name, types_invisible, use_cell_type_thresholding
            )

        if not fill_successful:
            return

        range_array = con_array.GetRange()
        min_con = range_array[0]
        max_con = range_array[1]
        # field_max = range_array[1]

        min_max_dict = self.get_min_max_metadata(scene_metadata=scene_metadata, field_name=field_name)
        min_range_fixed = min_max_dict["MinRangeFixed"]
        max_range_fixed = min_max_dict["MaxRangeFixed"]
        min_range = min_max_dict["MinRange"]
        max_range = min_max_dict["MaxRange"]

        # Note! should really avoid doing a getSetting with each step to speed up the rendering;
        # only update when changed in Prefs
        if min_range_fixed:
            min_con = min_range

        if max_range_fixed:
            max_con = max_range

        if show_contours:
            self.init_concentration_contours(
                dim=dim, con_array=con_array, isovalues=isovalues, min_con=min_con, max_con=max_con, numIsos=num_isos
            )
        else:
            self.init_concentration_outer_shell(
                dim=dim,
                con_array=con_array,
                cell_type_con=cell_type_con,
                isovalues=isovalues,
                min_con=min_con,
                max_con=max_con,
                numIsos=num_isos,
            )

        concentration_actor = actors_dict["concentration_actor"]

        concentration_actor.SetMapper(self.conMapper)

        self.init_min_max_actor(min_max_actor=actors_dict["min_max_text_actor"], range_array=range_array)

        if hex_flag:
            concentration_actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)

        if actor_specs.metadata is None:
            actor_specs.metadata = {"mapper": self.conMapper}
        else:
            actor_specs.metadata["mapper"] = self.conMapper

        if mdata.get("LegendEnable", default=False):
            self.init_legend_actors(actor_specs=actor_specs, drawing_params=drawing_params)

    def init_concentration_outer_shell(self, **kwds):
        """
        Extracts outer shell of visible cell types and colors the shell based on the value of
        concentration field
        """
        dim = kwds["dim"]
        con_array = kwds["con_array"]
        cell_type_con = kwds["cell_type_con"]
        min_con = kwds["min_con"]
        max_con = kwds["max_con"]

        vtk_shape_data = vtk.vtkImageData()
        # only add 2 if we're filling in an extra boundary (rf. FieldExtractor.cpp)
        vtk_shape_data.SetDimensions(dim[0] + 2, dim[1] + 2, dim[2] + 2)
        vtk_shape_data.GetPointData().SetScalars(cell_type_con)

        vtk_con_data = vtk.vtkImageData()
        # only add 2 if we're filling in an extra boundary (rf. FieldExtractor.cpp)
        vtk_con_data.SetDimensions(dim[0] + 2, dim[1] + 2, dim[2] + 2)
        vtk_con_data.GetPointData().SetScalars(con_array)

        mc = vtk.vtkMarchingCubes()
        # vtkFlyingEdges are a good alternative to marching cudes
        # mc = vtk.vtkFlyingEdges3D()
        mc.SetInputData(vtk_shape_data)
        # mc.ComputeNormalsOn()
        # mc.ComputeGradientsOn()
        # second value acts as threshold
        mc.SetValue(0, 1)

        probe = vtk.vtkProbeFilter()
        probe.SetInputConnection(mc.GetOutputPort())
        probe.SetSourceData(vtk_con_data)
        probe.Update()

        normals = vtk.vtkPolyDataNormals()
        normals.SetInputConnection(probe.GetOutputPort())

        self.conMapper = vtk.vtkPolyDataMapper()
        self.conMapper.ScalarVisibilityOn()
        self.conMapper.SetLookupTable(self.scalarLUT)
        self.conMapper.SetInputConnection(normals.GetOutputPort())
        self.conMapper.SetScalarRange(min_con, max_con)

    def init_concentration_contours(self, **kwds):
        """initializes contour visualization of concentration field in 3D"""
        dim = kwds["dim"]
        con_array = kwds["con_array"]
        isovalues = kwds["isovalues"]
        min_con = kwds["min_con"]
        max_con = kwds["max_con"]
        num_isos = kwds["num_isos"]

        uGrid = vtk.vtkStructuredPoints()
        # only add 2 if we're filling in an extra boundary (rf. FieldExtractor.cpp)
        uGrid.SetDimensions(dim[0] + 2, dim[1] + 2, dim[2] + 2)

        uGrid.GetPointData().SetScalars(con_array)

        voi = vtk.vtkExtractVOI()

        if VTK_MAJOR_VERSION >= 6:
            voi.SetInputData(uGrid)
        else:
            voi.SetInput(uGrid)

        # crop out the artificial boundary layer that we created
        voi.SetVOI(1, dim[0] - 1, 1, dim[1] - 1, 1, dim[2] - 1)

        iso_contour = vtk.vtkContourFilter()
        iso_contour.SetInputConnection(voi.GetOutputPort())

        iso_num = 0
        for iso_num, iso_val in enumerate(isovalues):
            try:
                iso_contour.SetValue(iso_num, iso_val)
            except:
                print(MODULENAME, " initScalarFieldDataActors(): cannot convert to float")

        if iso_num > 0:
            iso_num += 1

        # exclude the min,max for isovalues
        del_iso = (max_con - min_con) / (num_isos + 1)
        iso_val = min_con + del_iso
        for idx in range(num_isos):
            iso_contour.SetValue(iso_num, iso_val)
            iso_num += 1
            iso_val += del_iso

        # UGLY hack to NOT display anything since our attempt to RemoveActor (below) don't seem to work
        if iso_num == 0:
            iso_val = max_con + 1.0  # go just outside valid range
            iso_contour.SetValue(iso_num, iso_val)

        self.scalarLUT.SetTableRange([min_con, max_con])
        self.conMapper.SetInputConnection(iso_contour.GetOutputPort())
        self.conMapper.ScalarVisibilityOn()
        self.conMapper.SetLookupTable(self.scalarLUT)
        self.conMapper.SetScalarRange([min_con, max_con])

    def init_vector_field_actors(self, actor_specs, drawing_params=None):
        """
        initializes vector field actors for cartesian lattice
        :param actor_specs: {ActorSpecs}
        :param drawing_params: {DrawingParameters}
        :return: None
        """
        actors_dict = actor_specs.actors_dict

        field_dim = self.currentDrawingParameters.bsd.fieldDim
        field_name = drawing_params.fieldName
        field_type = drawing_params.fieldType.lower()
        scene_metadata = drawing_params.screenshot_data.metadata
        mdata = MetadataHandler(mdata=scene_metadata)

        dim = [field_dim.x, field_dim.y, field_dim.z]

        vector_grid = vtk.vtkUnstructuredGrid()

        points = vtk.vtkPoints()
        vectors = vtk.vtkFloatArray()
        vectors.SetNumberOfComponents(3)
        vectors.SetName("visVectors")

        points_int_addr = extract_address_int_from_vtk_object(vtkObj=points)
        vectors_int_addr = extract_address_int_from_vtk_object(vtkObj=vectors)

        fill_successful = False

        hex_flag = False

        if self.is_lattice_hex(drawing_params=drawing_params):
            hex_flag = True
            if field_type == "vectorfield":
                fill_successful = self.field_extractor.fillVectorFieldData3DHex(
                    points_int_addr, vectors_int_addr, field_name
                )
            elif field_type == "vectorfieldcelllevel":
                fill_successful = self.field_extractor.fillVectorFieldCellLevelData3DHex(
                    points_int_addr, vectors_int_addr, field_name
                )
        else:
            if field_type == "vectorfield":
                fill_successful = self.field_extractor.fillVectorFieldData3D(
                    points_int_addr,
                    vectors_int_addr,
                    field_name,
                )
            elif field_type == "vectorfieldcelllevel":
                fill_successful = self.field_extractor.fillVectorFieldCellLevelData3D(
                    points_int_addr,
                    vectors_int_addr,
                    field_name,
                )

        if not fill_successful:
            return

        vector_grid.SetPoints(points)
        vector_grid.GetPointData().SetVectors(vectors)

        cone = vtk.vtkConeSource()
        cone.SetResolution(5)
        cone.SetHeight(2)
        cone.SetRadius(0.5)
        # cone.SetRadius(4)

        range_array = vectors.GetRange(-1)

        min_magnitude = range_array[0]
        max_magnitude = range_array[1]

        min_max_dict = self.get_min_max_metadata(scene_metadata=scene_metadata, field_name=field_name)
        min_range_fixed = min_max_dict["MinRangeFixed"]
        max_range_fixed = min_max_dict["MaxRangeFixed"]
        min_range = min_max_dict["MinRange"]
        max_range = min_max_dict["MaxRange"]

        # Note! should really avoid doing a getSetting with each step to speed up the rendering;
        # only update when changed in Prefs
        if min_range_fixed:
            min_magnitude = min_range

        if max_range_fixed:
            max_magnitude = max_range

        glyphs = vtk.vtkGlyph3D()

        if VTK_MAJOR_VERSION >= 6:
            glyphs.SetInputData(vector_grid)
        else:
            glyphs.SetInput(vector_grid)

        glyphs.SetSourceConnection(cone.GetOutputPort())
        # glyphs.SetScaleModeToScaleByVector()
        # glyphs.SetColorModeToColorByVector()

        # scaling arrows here ArrowLength indicates scaling factor not actual length
        # glyphs.SetScaleFactor(Configuration.getSetting("ArrowLength"))

        vector_field_actor = actors_dict["vector_field_actor"]

        # scaling factor for an arrow - ArrowLength indicates scaling factor not actual length
        arrowScalingFactor = mdata.get("ArrowLength", default=1.0)

        if mdata.get("FixedArrowColorOn", default=False):
            glyphs.SetScaleModeToScaleByVector()

            dataScalingFactor = max(abs(min_magnitude), abs(max_magnitude))

            if dataScalingFactor == 0.0:
                # in this case we are plotting 0 vectors and in this case data scaling factor will be set to 1
                dataScalingFactor = 1.0

            glyphs.SetScaleFactor(arrowScalingFactor / dataScalingFactor)

            # coloring arrows
            arrow_color = to_vtk_rgb(mdata.get("ArrowColor", data_type="color"))
            vector_field_actor.GetProperty().SetColor(arrow_color)

        else:
            glyphs.SetColorModeToColorByVector()
            glyphs.SetScaleFactor(arrowScalingFactor)

        self.glyphsMapper.SetInputConnection(glyphs.GetOutputPort())
        self.glyphsMapper.SetLookupTable(self.scalarLUT)

        self.glyphsMapper.SetScalarRange([min_magnitude, max_magnitude])

        vector_field_actor.SetMapper(self.glyphsMapper)

        self.init_min_max_actor(min_max_actor=actors_dict["min_max_text_actor"], range_array=range_array)

        if hex_flag:
            vector_field_actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)

    def init_outline_actors(self, actor_specs, drawing_params=None):
        """
        Initializes outline actors for hex actors
        :param actor_specs: {ActorSpecs}
        :param drawing_params: {DrawingParameters}
        :return: None
        """
        actors_dict = actor_specs.actors_dict
        field_dim = self.currentDrawingParameters.bsd.fieldDim
        scene_metadata = drawing_params.screenshot_data.metadata
        mdata = MetadataHandler(mdata=scene_metadata)

        outline_data = vtk.vtkImageData()

        outline_data.SetDimensions(field_dim.x + 1, field_dim.y + 1, field_dim.z + 1)

        outline = vtk.vtkOutlineFilter()

        if VTK_MAJOR_VERSION >= 6:
            outline.SetInputData(outline_data)
        else:
            outline.SetInput(outline_data)

        outline_mapper = vtk.vtkPolyDataMapper()
        outline_mapper.SetInputConnection(outline.GetOutputPort())

        outline_actor = actors_dict["outline_actor"]

        outline_actor.SetMapper(outline_mapper)

        # lattice_type_str = self.get_lattice_type_str()
        # if lattice_type_str.lower() == 'hexagonal':
        if self.is_lattice_hex(drawing_params=drawing_params):
            outline_actor.SetScale(self.xScaleHex, self.yScaleHex, self.zScaleHex)

        outline_color = to_vtk_rgb(mdata.get("BoundingBoxColor", data_type="color"))
        outline_actor.GetProperty().SetColor(*outline_color)

    def init_axes_actors(self, actor_specs, drawing_params=None):
        """
        Initializes outline actors for hex actors
        :param actor_specs: {ActorSpecs}
        :param drawing_params: {DrawingParameters}
        :return: None
        """
        actors_dict = actor_specs.actors_dict
        field_dim = self.currentDrawingParameters.bsd.fieldDim
        scene_metadata = drawing_params.screenshot_data.metadata
        mdata = MetadataHandler(mdata=scene_metadata)

        axes_actor = actors_dict["axes_actor"]
        axes_color = to_vtk_rgb(mdata.get("AxesColor", data_type="color"))

        tprop = vtk.vtkTextProperty()
        tprop.SetColor(axes_color)
        tprop.ShadowOn()

        axes_actor.SetNumberOfLabels(4)  # number of labels

        # lattice_type_str = self.get_lattice_type_str()
        # if lattice_type_str.lower() == 'hexagonal':
        if self.is_lattice_hex(drawing_params=drawing_params):
            axes_actor.SetBounds(
                0, field_dim.x, 0, field_dim.y * math.sqrt(3.0) / 2.0, 0, field_dim.z * math.sqrt(6.0) / 3.0
            )
        else:
            axes_actor.SetBounds(0, field_dim.x, 0, field_dim.y, 0, field_dim.z)

        axes_actor.SetLabelFormat("%6.4g")
        axes_actor.SetFlyModeToOuterEdges()
        axes_actor.SetFontFactor(1.5)

        # axesActor.GetProperty().SetColor(float(color.red())/255,float(color.green())/255,float(color.blue())/255)
        axes_actor.GetProperty().SetColor(axes_color)

        xAxisActor = axes_actor.GetXAxisActor2D()
        # xAxisActor.RulerModeOn()
        # xAxisActor.SetRulerDistance(40)
        # xAxisActor.SetRulerMode(20)
        # xAxisActor.RulerModeOn()
        xAxisActor.SetNumberOfMinorTicks(3)

    def init_fpp_links_actors(self, actor_specs, drawing_params=None):
        """
        initializes fpp links actors
        :param actor_specs:
        :param drawing_params:
        :return: None
        """

        fpp_plugin = CompuCell.getFocalPointPlasticityPlugin()
        if not fpp_plugin:
            print("    fppPlugin is null, returning")
            return

        actors_dict = actor_specs.actors_dict
        field_dim = self.currentDrawingParameters.bsd.fieldDim
        scene_metadata = drawing_params.screenshot_data.metadata
        mdata = MetadataHandler(mdata=scene_metadata)

        try:
            inventory = self.currentDrawingParameters.bsd.sim.getPotts().getCellInventory()
        except AttributeError:
            raise AttributeError("Could not access Potts object")

        cell_list = CellList(inventory)

        points = vtk.vtkPoints()
        lines = vtk.vtkCellArray()

        pt_counter = 0

        for cell in cell_list:
            vol = cell.volume
            if vol < self.eps:
                continue

            mid_com = np.array([cell.xCOM, cell.yCOM, cell.zCOM], dtype=float)

            for fppd in InternalFocalPointPlasticityDataList(fpp_plugin, cell):
                pt_counter = self.add_link(
                    field_dim=field_dim, fppd=fppd, mid_com=mid_com, pt_counter=pt_counter, lines=lines, points=points
                )

            for fppd in FocalPointPlasticityDataList(fpp_plugin, cell):
                pt_counter = self.add_link(
                    field_dim=field_dim, fppd=fppd, mid_com=mid_com, pt_counter=pt_counter, lines=lines, points=points
                )

        fpp_links_pd = vtk.vtkPolyData()
        fpp_links_pd.SetPoints(points)
        fpp_links_pd.SetLines(lines)

        fpp_links_actor = actors_dict["fpp_links_actor"]

        if VTK_MAJOR_VERSION >= 6:
            self.FPPLinksMapper.SetInputData(fpp_links_pd)
        else:
            fpp_links_pd.Update()
            self.FPPLinksMapper.SetInput(fpp_links_pd)

        fpp_links_actor.SetMapper(self.FPPLinksMapper)
        fpp_links_color = to_vtk_rgb(mdata.get("FPPLinksColor", data_type="color"))

        # coloring borders
        fpp_links_actor.GetProperty().SetColor(*fpp_links_color)

    def add_link(self, field_dim, fppd, mid_com, pt_counter, lines, points) -> int:
        """
        Draws single link in 3D. Returns updated point counter

        :param field_dim:
        :param fppd:
        :param mid_com: link begin
        :param pt_counter: point counter
        :param lines: vtk lines structure that holds line specification
        :param points: vtk points sstructure
        :return: end point counter
        """

        n_cell = fppd.neighborAddress

        n_mid_com = np.array([n_cell.xCOM, n_cell.yCOM, n_cell.zCOM], dtype=float)

        naive_actual_dist = np.linalg.norm(mid_com - n_mid_com)
        inv_dist = self.invariant_distance(p1=mid_com, p2=n_mid_com, dim=field_dim)
        if abs((inv_dist - naive_actual_dist) / (naive_actual_dist + epsilon)) > 10 * epsilon:
            # if naive distance is different than invariant distance then we are dealing with link that is wrapped
            # if naive_actual_dist > fppd.maxDistance:  # implies we have wraparound (via periodic BCs)
            # we are drawing links that currently stick out of the lattice.
            inv_dist_vec = self.invariant_distance_vector(p1=mid_com, p2=n_mid_com, dim=field_dim)

            # inv_dist_vec = self.unconditional_invariant_distance_vector(p1=mid_com,
            #                                                             p2=n_mid_com,
            #                                                             dim=field_dim)
            link_begin = mid_com
            link_end = link_begin + inv_dist_vec

            points.InsertNextPoint(mid_com[0], mid_com[1], mid_com[2])
            points.InsertNextPoint(link_end[0], link_end[1], link_end[2])
            # our line has 2 points
            lines.InsertNextCell(2)
            lines.InsertCellPoint(pt_counter)
            lines.InsertCellPoint(pt_counter + 1)
            pt_counter += 2

        # link didn't wrap around on lattice
        else:
            points.InsertNextPoint(mid_com[0], mid_com[1], mid_com[2])
            points.InsertNextPoint(n_mid_com[0], n_mid_com[1], n_mid_com[2])
            # our line has 2 points
            lines.InsertNextCell(2)
            lines.InsertCellPoint(pt_counter)
            lines.InsertCellPoint(pt_counter + 1)

            pt_counter += 2

        return pt_counter
