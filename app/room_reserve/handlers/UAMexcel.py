import pandas as pd
import json


class ExcelToJsonProcessor:
    def excel_to_json(self, file):
        try:
            df = pd.read_excel(file)
            result = []

            for index, row in df.iterrows():
                # Combine date and time for start_time and end_time
                start_datetime = ""
                end_datetime = ""

                if pd.notna(row.iloc[2]) and pd.notna(row.iloc[3]):
                    start_datetime = f"{row.iloc[2].strftime('%Y-%m-%d')} {row.iloc[3].strftime('%H:%M')}"

                if pd.notna(row.iloc[2]) and pd.notna(row.iloc[4]):
                    end_datetime = f"{row.iloc[2].strftime('%Y-%m-%d')} {row.iloc[4].strftime('%H:%M')}"

                entry = {
                    "entry*id": f"entry*{index + 1}",
                    "data": {
                        "name": row.iloc[0] if pd.notna(row.iloc[0]) else "",
                        "name_eng": row.iloc[1] if pd.notna(row.iloc[1]) else "",
                        "start_time": start_datetime,
                        "end_time": end_datetime,
                    },
                }
                result.append(entry)

            json_string = json.dumps(result, indent=2, ensure_ascii=False)
            return json_string
        except Exception as e:
            return str(e)
