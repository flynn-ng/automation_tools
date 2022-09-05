import pandas as pd
import re


class TagGenerator:
    def __init__(self, file_name, extension='xlsx', header=None):
        self.file_name = file_name
        self.extension = extension
        self.header = header
        self.sheets = pd.read_excel(f'{self.file_name}.{self.extension}', sheet_name=None, header=self.header).items()

    @staticmethod
    def sequence(df, name):
        sel_df = pd.DataFrame()
        stt_df = pd.DataFrame()
        sp_df = pd.DataFrame()
        spp_df = pd.DataFrame()
        df['DATATYPE'] = name
        sel_df['NAME'] = df['NAME'].apply(lambda x: "OP_" + x)
        sel_df['DATATYPE'] = "RW_Selection"
        stt_df['NAME'] = df['NAME'].apply(lambda x: x + "_S")
        stt_df['DATATYPE'] = "Status"
        sp_df['NAME'] = df['NAME'].apply(lambda x: x + "_SP")
        sp_df['DATATYPE'] = "SETPOINTS[100]"
        spp_df['NAME'] = df['NAME'].apply(lambda x: x + "_HMI_SP")
        spp_df['DATATYPE'] = "SETPOINT100"
        df = pd.concat([df, sel_df, stt_df, sp_df, spp_df])
        df['ATTRIBUTES'] = "(Constant := false, ExternalAccess := Read/Write)"
        return df

    @staticmethod
    def motor_ao(df, name):
        motor_ao_df = pd.DataFrame()
        motor_ao_df['NAME'] = df['NAME'].apply(lambda x: x + "_SC")
        motor_ao_df['DATATYPE'] = "RW_AO"
        motor_ao_df['DESCRIPTION'] = df['DESCRIPTION']
        df['DATATYPE'] = name
        df = pd.concat([df, motor_ao_df])
        df['ATTRIBUTES'] = "(Constant := false, ExternalAccess := Read/Write)"
        return df

    @staticmethod
    def ai_and_di(df, name):
        alm_df = pd.DataFrame()
        alm_df['NAME'] = df['NAME'].apply(lambda x: x + "_ALM")
        if re.search("AI", name):
            alm_df['DATATYPE'] = "ALARM_ANALOG"
        else:
            alm_df['DATATYPE'] = "ALARM_DIGITAL"
        df['DATATYPE'] = name
        df = pd.concat([df, alm_df])
        df['ATTRIBUTES'] = "(Constant := false, ExternalAccess := Read/Write)"
        return df

    @staticmethod
    def rw(df, name):
        df['DATATYPE'] = name
        df['ATTRIBUTES'] = "(Constant := false, ExternalAccess := Read/Write)"
        return df

    @staticmethod
    def default(df, name):
        df['DATATYPE'] = name
        df['ATTRIBUTES'] = "(RADIX := Decimal, Constant := true, ExternalAccess := Read/Write)"
        return df

    def generate(self):
        result_df = pd.DataFrame()
        for sheet_name, df in self.sheets:
            if not df.empty:
                df = df.rename(columns={0: "NAME", 1: "DESCRIPTION"})
                if re.search("Sequence", sheet_name):
                    df = self.sequence(df, sheet_name)
                elif re.search("AI", sheet_name) or re.search("DI", sheet_name):
                    df = self.ai_and_di(df, sheet_name)
                elif re.search("Motor", sheet_name):
                    df = self.motor_ao(df, sheet_name)
                elif re.search("RW_", sheet_name):
                    df = self.rw(df, sheet_name)
                else:
                    df = self.default(df, sheet_name)
                df['TYPE'] = "TAG"
                df['SCOPE'] = ""
                df['SPECIFIER'] = ""
                result_df = pd.concat([df, result_df])
        return result_df

    def csv_out(self):
        self.generate().to_csv('out.csv',
                               columns=['TYPE', 'SCOPE', 'NAME', 'DESCRIPTION', 'DATATYPE', 'SPECIFIER', 'ATTRIBUTES'],
                               index=False)

        #     if df.empty:
        #         continue
        #     else:
        #         df = df.rename(columns={0: "NAME", 1: "DESCRIPTION"})
        #         df['DATATYPE'] = sheet_name
        #         if self.is_setpoint:
        #             addition_setpoint = pd.DataFrame()
        #             addition_setpoint['NAME'] = df['NAME'].replace("_HMI", "")
        #             addition_setpoint['DATATYPE'] = df['DATATYPE'].repalce("100", "S[100]")
        #             df = pd.concat([df, addition_setpoint])
        #         if self.is_default_datatype:
        #             df['ATTRIBUTES'] = "(RADIX := Decimal, Constant := true, ExternalAccess := Read/Write)"
        #         else:
        #             df['ATTRIBUTES'] = "(Constant := false, ExternalAccess := Read/Write)"
        #         df['TYPE'] = "TAG"
        #         df['SCOPE'] = ""
        #         df['SPECIFIER'] = ""
        #         result_df = pd.concat([df, result_df])
        # return result_df.to_csv('out.csv',
        #                         columns=['TYPE', 'SCOPE', 'NAME', 'DESCRIPTION', 'DATATYPE', 'SPECIFIER',
        #                                  'ATTRIBUTES'],
        #                         index=False)


v = TagGenerator('Tag_Tool')
v.generate()
v.csv_out()
# print(f'remark,Phong,,,,,\n0.3,,,,,,\n{x.generate()}')
