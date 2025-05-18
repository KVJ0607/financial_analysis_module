import pickle 
HKEX_TONEMERGE_ACAR3_HCAR3='example_data/no_hkex_tonemerge_acar3_hcar3.pkl'

def get_hkex_tonemerge_acar3_hcar3()->dict[int,list[tuple]]:    
    with open(HKEX_TONEMERGE_ACAR3_HCAR3, 'rb') as file:
        return_dict = pickle.load(file)
    return return_dict

return_dict = get_hkex_tonemerge_acar3_hcar3()
print(return_dict.keys() )



def tonemerge_car3_analysis(hkex_tonemerge_acar3_hcar3:dict[int,list[tuple]],no_hkex_tonemerge_acar3_hcar3:dict[int,list[tuple]]): 
    conn = sqlite3.connect(COMPANIES_DB)
    cursor = conn.cursor()   
    try: 
        hkex_result_dict={
            "pearson":{},
            "spearman":{}
        }
        for cp_id in range(1,150): 
            if cp_id in SKIP_ID: 
                continue

            data=hkex_tonemerge_acar3_hcar3[cp_id]

            # Convert the list of tuples into a pandas DataFrame
            df = pd.DataFrame(data, columns=['net_tonescore', 'positive_tonescore', 'negative_tonescore', 'acar3', 'hcar3'])

            # Calculate Pearson correlation coefficients - assumes linear relationship and data is normally distributed
            pearson_corr = df.corr(method='pearson')
            

            # Calculate Spearman correlation coefficients - makes no assumption about the distribution of the data
            spearman_corr = df.corr(method='spearman')

            hkex_result_dict["pearson"][cp_id]=pearson_corr
            hkex_result_dict["spearman"][cp_id]=spearman_corr
        
                
        with open(HKEX_TONECAR_CORRELATION_RESULT, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['pearson','spearman'])
            for cp_id_ in range(1,150): 
                if cp_id_ in SKIP_ID: 
                    continue
                pearson_=hkex_result_dict['pearson'][cp_id_]
                spearman_=hkex_result_dict['spearman'][cp_id_]
                h_code_=get_company_code(cursor,cp_id)
                writer.writerow([h_code_,pearson_,spearman_])


        no_hkex_result_dict={
            "pearson":{},
            "spearman":{}
        }
        for cp_id in range(1,150): 
            if cp_id in SKIP_ID: 
                continue

            no_hkex_data=no_hkex_tonemerge_acar3_hcar3[cp_id]

            # Convert the list of tuples into a pandas DataFrame
            df = pd.DataFrame(no_hkex_data, columns=['net_tonescore', 'positive_tonescore', 'negative_tonescore', 'acar3', 'hcar3'])

            # Calculate Pearson correlation coefficients - assumes linear relationship and data is normally distributed
            pearson_corr = df.corr(method='pearson')
            

            # Calculate Spearman correlation coefficients - makes no assumption about the distribution of the data
            spearman_corr = df.corr(method='spearman')

            no_hkex_result_dict["pearson"][cp_id]=pearson_corr
            no_hkex_result_dict["spearman"][cp_id]=spearman_corr
        
                
        with open(NO_HKEX_TONECAR_CORRELATION_RESULT, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['pearson','spearman'])
            for cp_id_ in range(1,150): 
                if cp_id_ in SKIP_ID: 
                    continue
                pearson_=no_hkex_result_dict['pearson'][cp_id_]
                spearman_=no_hkex_result_dict['spearman'][cp_id_]
                h_code_=get_company_code(cursor,cp_id)
                writer.writerow([h_code_,pearson_,spearman_])
    except Exception as e: 
        conn.close()
        raise(Exception(e))
        
    return hkex_result_dict,no_hkex_result_dict
