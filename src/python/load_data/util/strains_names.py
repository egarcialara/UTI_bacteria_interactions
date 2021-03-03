def change_names(df, list_, rows, cols):
    ''' description function'''
    for i in range(0, len(list_)):
        if "ent" in list_[i]:
            list_[i] = 'Ent'
        elif 'coli' in list_[i]:
            list_[i] = "Ecoli"
        elif 'pseu' in list_[i]:
            list_[i] = 'Ps'
        elif 'staph' in list_[i]:
            list_[i] = 'St'
        elif 'mirab' in list_[i]:
            list_[i] = 'Pm'
        elif 'morg' in list_[i]:
            list_[i] = 'MM'
        elif 'kleb' in list_[i] or 'serrat' in list_[i] or 'citro' in list_[i] or 'panto' in list_[i]:
            list_[i] = 'KECS'

    if rows:
        df.index = list_
    if cols:
        df.columns = list_
    return df