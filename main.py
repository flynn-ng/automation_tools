from lxml import etree
from lxml.builder import E
from tag import TagGenerator
import cssselect
import pandas as pd

tags = TagGenerator('Tag_Tool')
df = tags.generate()
# print(type(df))
parser = etree.XMLParser(strip_cdata=False)

with open('Devices.xml', "rb") as source:
    tree = etree.parse(source, parser)
controller = tree.find('//Controller')
for child in controller.getchildren():
    if child.tag in ['Tags', 'AddOnInstructionDefinitions']:
        controller.remove(child)
# print(etree.tostring(tree))
routines_node = tree.find('//Controller/Programs/Program/Routines')
routines = tree.findall('//Controller/Programs/Program/Routines/Routine')
# print(routines_node)
for routine in routines:
    if routine.attrib['Name'] != 'MainRoutine':
        for child in routine.getchildren():
            routine.remove(child)
    if routine.attrib['Name'] == 'Call_AI':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")), E.Text(
                    etree.CDATA(f"{value['DATATYPE']}({value['NAME']},TaskHoldFault.DN,sPowerUp.TT,Simulation);")),
                         Number=f"{index}", Type="N") for index, value in df.loc[df['DATATYPE'] == 'RW_AI'].iterrows()]
            )
        )
    elif routine.attrib['Name'] == 'Call_AI_ALM':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")), E.Text(
                    etree.CDATA(
                        f"ALMA({value['NAME']}_ALM,{value['NAME']}.In,{value['NAME']}_ALM.ProgAckAll,{value['NAME']}_ALM.ProgDisable,{value['NAME']}_ALM.ProgEnable);")),
                         Number=f"{index}", Type="N") for index, value in df.loc[df['DATATYPE'] == 'RW_AI'].iterrows()]
            )
        )
    elif routine.attrib['Name'] == 'Call_AO':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")),
                         E.Text(etree.CDATA(f"RW_AO({value['NAME']},sPowerUp.TT,TaskHoldFault.DN);")),
                         Number=f'{index}', Type="N") for
                  index, value in df.loc[df['DATATYPE'] == 'RW_AO'].iterrows()]
            )
        )
    elif routine.attrib['Name'] == 'Call_DI':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")), E.Text(
                    etree.CDATA(f"RW_DI({value['NAME']},sHoldFault.DN,Simulation,{value['NAME']}_ALM.InAlrm);")),
                         Number=f"{index}", Type="N") for index, value in df.loc[df['DATATYPE'] == 'RW_DI'].iterrows()]
            )
        )
    elif routine.attrib['Name'] == 'Call_DO':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")), E.Text(
                    etree.CDATA(
                        f"RW_DO({value['NAME']},sPowerUp.TT,FaultSimT.DN,FaultSimT.TT,Simulation,s4SecondPulse);")),
                         Number=f"{index}", Type="N") for index, value in df.loc[df['DATATYPE'] == 'RW_DO'].iterrows()]
            )
        )
    elif routine.attrib['Name'] == 'Call_MOTOR':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")), E.Text(
                    etree.CDATA(
                        f"RW_Motor({value['NAME']},sPowerUp.DN,sPowerUp.TT,sRateDevice,FaultSimT.DN,Simulation,sHoldFault.DN,s1SecondPulse,s4SecondPulse,bhno,sPowerFactor,sLineVolts);")),
                         Number=f"{index}", Type="N") for index, value in
                  df.loc[df['DATATYPE'] == 'RW_Motor'].iterrows()]
            )
        )
    elif routine.attrib['Name'] == 'Call_VALVE':
        routine.append(
            E.RLLContent(
                *[E.Rung(E.Comment(etree.CDATA(f"=={value['NAME']} - {value['DESCRIPTION']}==")), E.Text(
                    etree.CDATA(
                        f"RW_Valve({value['NAME']},sPowerUp.TT,sRateDevice,FaultSimT.DN,Simulation,sHoldFault.DN,FaultSimT.TT,s4SecondPulse,);")),
                         Number=f"{index}", Type="N") for index, value in
                  df.loc[df['DATATYPE'] == 'RW_Valve'].iterrows()]
            )
        )
        # print("hello")
        # print([idx for idx, (index, value) in enumerate(df.loc[df['DATATYPE'] == 'RW_AO'].iterrows())])
        # for index, value in df.loc[df['DATATYPE'] == 'RW_AI'].iterrows():
        #     print(value['NAME'])
        # routine.append(
        #     E.RLLContent(
        #         E.Rung(
        #             E.Comment(etree.CDATA("==Bom dep trai")), E.Text(etree.CDATA("hhahahhaha")), Number="0", Type="N")))
        # print(etree.tostring(routine))
        # print(etree.tostring(tree, pretty_print=True))
        # et = etree.ElementTree(tree)
        # print(etree.tostring())
tree.write('output.l5x', xml_declaration=True, encoding='utf-8', standalone='yes')
# tags = tree.findall('//Controller/Tags/Tag')
# tag = E.Tag(E.Descriptions(etree.CDATA('Ditconme')), Name="XINCHAO", TagType="ConCac")
#
# tags_node.append(tag)
#
# print(etree.tostring(tags_node, pretty_print=True))

# print(tags)
# routines = tree.findall('//Programs//Routines/Routine')
# for routine in routines:
#     print(routine.attrib)
# program.find('.//Routines')

# root = tree.getroot()
# print(cssselect.Selector('Program'))
