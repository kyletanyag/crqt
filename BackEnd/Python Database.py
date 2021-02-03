import pandas as pd
CVD_ID = []
description = []
base_score_V2 = []
impact_score_V2=[]
exploitability_score_V2 = []
base_score_V3 = []
impact_score_V3=[]
exploitability_score_V3 = []


def Dataframe_Creator(file):
    for i in file["CVE_Items"]:
        CVD_ID.append(i["cve"]['CVE_data_meta']['ID'])
        description.append(f"{i['cve']['description']['description_data'][0]['value']}")
        try:
            base_score_V2.append(i['impact']['baseMetricV2']['cvssV2']['baseScore'])
            impact_score_V2.append(i['impact']['baseMetricV2']['impactScore'])
            exploitability_score_V2.append(i['impact']['baseMetricV2']['exploitabilityScore'])
            base_score_V3.append(i['impact']['baseMetricV3']['cvssV3']['baseScore'])
            impact_score_V3.append(i['impact']['baseMetricV3']['impactScore'])
            exploitability_score_V3.append(i['impact']['baseMetricV3']['exploitabilityScore'])

        except KeyError:
            base_score_V2.append("Not Provided")
            impact_score_V2.append("Not Provided")
            exploitability_score_V2.append("Not Provided")
            base_score_V3.append("Not Provided")
            impact_score_V3.append("Not Provided")
            exploitability_score_V3.append("Not Provided")

    dict_data = {'CVE ID': CVD_ID,"Description": description, "V2 base score":base_score_V2, "V2 impact score": impact_score_V2,
             "V2 exploitability score": exploitability_score_V2,"V3 base score":base_score_V3,
             "V3 impact score": impact_score_V3, "V3 exploitability score": exploitability_score_V3}

    df = pd.DataFrame.from_dict(dict_data)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 10000)
    pd.set_option('display.colheader_justify', "center")
    pd.set_option('display.precision', 2)
    return df
###dataframe 2018 data added to the beginning of the excel document
file = pd.read_json(r"C:\Users\Cierra\Downloads\Capstone Data\d2018.json")
dataframe_2018=Dataframe_Creator(file)
print(len(dataframe_2018))
dataframe_2018.to_excel(r'C:\Users\Cierra\Documents\Python Scripts\CapstoneData2021.xlsx')

####dataframe 2019 data added to the end of the excel document
file_2019 = pd.read_json(r"C:\Users\Cierra\Downloads\Capstone Data\d2019.json")
dataframe_2019=Dataframe_Creator(file_2019)
print(len(dataframe_2019))
writer = pd.ExcelWriter(r'C:\Users\Cierra\Documents\Python Scripts\CapstoneData2021.xlsx')
dataframe_2019.to_excel(writer)
writer.save()

####dataframe 2020 data added to the end of the excel
file_2020 = pd.read_json(r"C:\Users\Cierra\Downloads\Capstone Data\d2020.json")
dataframe_2020=Dataframe_Creator(file_2020)
print(len(dataframe_2020))
writer = pd.ExcelWriter(r'C:\Users\Cierra\Documents\Python Scripts\CapstoneData2021.xlsx')
dataframe_2020.to_excel(writer)
writer.save()




