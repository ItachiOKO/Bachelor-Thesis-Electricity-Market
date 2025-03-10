import pandas as pd 


def export_results(df, results_file_name_excel, results_file_name_pickle):
    df.to_pickle(results_file_name_pickle)
    df.index = df.index.tz_localize(None)
    attrs_df = pd.DataFrame(list(df.attrs.items()), columns=['Attribute', 'Value'])
    with pd.ExcelWriter(results_file_name_excel, engine='xlsxwriter') as writer:
        attrs_df.to_excel(writer, sheet_name='Attributes', index=False)
        df.to_excel(writer, sheet_name='Data')