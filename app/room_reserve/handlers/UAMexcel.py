import pandas as pd
import json

class ExcelToJsonProcessor:
    def excel_to_json(self, file):
        try:
            df = pd.read_excel(file)
            result = []
            
            for index, row in df.iterrows():
                entry = {
                    "entry*id": f"entry*{index + 1}",
                    "data": {
                        "name": row.iloc[0] if pd.notna(row.iloc[0]) else "",
                        "name_eng": row.iloc[1] if pd.notna(row.iloc[1]) else "",
                        "date": row.iloc[2].strftime('%Y-%m-%d') if pd.notna(row.iloc[2]) else "",
                        "start_time": row.iloc[3].strftime('%H:%M') if pd.notna(row.iloc[3]) else "",
                        "end_time": row.iloc[4].strftime('%H:%M') if pd.notna(row.iloc[4]) else "",
                        "event_name": row.iloc[5] if pd.notna(row.iloc[5]) else ""
                    }
                }
                result.append(entry)
            
            json_string = json.dumps(result, indent=2, ensure_ascii=False)
            return json_string
        except Exception as e:
            return str(e)