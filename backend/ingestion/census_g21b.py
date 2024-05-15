from constants import CENSUS_G21B

def insert(es, bulker, data):       
    if not es.indices.exists(index=CENSUS_G21B):
        return f'{CENSUS_G21B} index does not exist'

    # Use count API to get the number of documents in the index
    document_count = es.count(index=CENSUS_G21B)['count']

    if(document_count > 0):
        return f'{CENSUS_G21B} already has data. Please delete before attempting re-insertion.'

    try:
        inserts = []
        for _, row in data.items():
            insert = {
                'create': {
                "assistance_needed_asthma": row['assistance_needed_asthma'],
                "assistance_needed_copd": row['assistance_needed_copd'],
                "employed_copd":row['employed_copd'] ,
                "gccsa_code":row['gccsa_code'] ,
                "gccsa_name":row['gccsa_name'] ,
                "total_asthma":row['total_asthma'] ,
                "total_copd":row['total_copd'] ,
                "unemployed_asthma":row['unemployed_asthma'] ,
                "unemployed_copd":row['unemployed_copd'] ,
                "weekly_income_1000_1749_asthma":row['weekly_income_1000_1749_asthma'] ,
                "weekly_income_1000_1749_copd":row['weekly_income_1000_1749_copd'] ,
                "weekly_income_1750_2999_asthma":row['weekly_income_1750_2999_asthma'] ,
                "weekly_income_1750_2999_copd":row['weekly_income_1750_2999_copd'] ,
                "weekly_income_1_299_asthma":row['weekly_income_1_299_asthma'] ,
                "weekly_income_1_299_copd":row['weekly_income_1_299_copd'] ,
                "weekly_income_3000_asthma":row['weekly_income_3000_asthma'] ,
                "weekly_income_3000_copd":row['weekly_income_3000_copd'] ,
                "weekly_income_300_649_asthma":row['weekly_income_300_649_asthma'],
                "weekly_income_300_649_copd":row['weekly_income_300_649_copd'],
                "weekly_income_650_999_asthma":row['weekly_income_650_999_asthma'],
                "weekly_income_650_999_copd":row['weekly_income_650_999_copd'] ,
                "weekly_income_nil_asthma":row['weekly_income_nil_asthma'],
                "weekly_income_nil_copd":row['weekly_income_nil_copd'] 
                }
            }
            inserts.append(insert)
            
        result = bulker.bulk(es, inserts, index=CENSUS_G21B)
    except Exception as e:
        return f'{e}'
    return result