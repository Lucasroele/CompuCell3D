

#include "ChickTypePlugin.h"
#include "ChickNonCondensingTransition.h"
#include "ChickCondensingTransition.h"
#include <CompuCell3D/Automaton/CellType.h>
#include <CompuCell3D/ClassRegistry.h>
using namespace CompuCell3D;

#include <CompuCell3D/Simulator.h>
#include <CompuCell3D/Potts3D/Potts3D.h>
#include <CompuCell3D/steppables/PDESolvers/DiffusableVector.h>

#include <XMLCereal/XMLPullParser.h>
#include <XMLCereal/XMLSerializer.h>

#include <BasicUtils/BasicString.h>
#include <BasicUtils/BasicException.h>

#include <iostream>
using namespace std;

ChickTypePlugin::ChickTypePlugin() {}

ChickTypePlugin::~ChickTypePlugin() {}

void ChickTypePlugin::init(Simulator *simulator) {
           sim = simulator;
           potts = simulator->getPotts();
           potts->registerCellGChangeWatcher(this);
           potts->registerAutomaton(this);
           classType = new CellType();
           classType->addTransition(new ChickNonCondensingTransition(1));
           classType->addTransition(new ChickCondensingTransition(2));
}

float ChickTypePlugin::getConcentration(Point3D pt) {
    return
           ((DiffusableVector<float>*)sim->getClassRegistry()->getStepper(fieldSource))->getConcentrationField(fieldName)->get(pt);
}

unsigned char ChickTypePlugin::getCellType(const CellG *cell) const {
  if (!cell) return 0;
  else if (const_cast<CellG*>(cell)->type == 0)
      const_cast<CellG*>(cell)->type = 1;
  return const_cast<CellG*>(cell)->type; 
}

string ChickTypePlugin::getTypeName(const char type) const {
  switch (type) {
  case 0: return "Medium";
  case 1: return "NonCondensing";
  case 2: return "Condensing";
  default: THROW(string("Unknown cell type ") + BasicString(type) + "!");
  }
}

unsigned char ChickTypePlugin::getTypeId(const string typeName) const {
  if (typeName == "Medium") return 0;
  else if (typeName == "NonCondensing") return 1;
  else if (typeName == "Condensing") return 2;
  else THROW(string("Unknown cell type ") + typeName + "!");
}

void ChickTypePlugin::readXML(XMLPullParser &in) {
  cerr << "**** IN READXML ****" << endl;
  in.skip(TEXT);

  while (in.check(START_ELEMENT)) {
    if (in.getName() == "Threshold") {
      threshold = BasicString::parseDouble(in.matchSimple());
    }
    else if (in.getName() == "ChemicalField") {
      fieldSource = in.getAttribute("Source").value;
      fieldName = in.getAttribute("Name").value;
      in.matchSimple();
    }
    else {
      throw BasicException(string("Unexpected element '") + in.getName() +
                           "'!", in.getLocation());
    }

    in.skip(TEXT);
  }
  cerr << "FIELDSOURCE IN READXML: " << fieldSource << endl;
}

void ChickTypePlugin::writeXML(XMLSerializer &out) {
}
