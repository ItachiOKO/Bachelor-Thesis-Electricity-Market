import pandas as pd 
from utils import convert_datetime_to_string


def export_results(df, results_file_name_excel, results_file_name_pickle):
    df.to_pickle(results_file_name_pickle)
    formated_df = convert_datetime_to_string(df)
    attrs_df = pd.DataFrame(list(formated_df.attrs.items()), columns=['Attribute', 'Value'])
    with pd.ExcelWriter(results_file_name_excel, engine='xlsxwriter') as writer:
        attrs_df.to_excel(writer, sheet_name='Attributes', index=False)
        formated_df.to_excel(writer, sheet_name='Data')