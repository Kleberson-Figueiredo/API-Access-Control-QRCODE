from datetime import datetime,timedelta
data_atual = datetime.now()
data_filtro = data_atual - timedelta(days=6)

def add_hours(data):
    if type(data) == str:
        data = datetime.strptime(data, '%Y-%m-%d')+timedelta(hours=23)
        return data
    return data



def normalize_path_params(datamin=data_filtro,datamax=data_atual\
                        ,status=None, codusuario=None, limit=50, offset=0, **dados):
    if codusuario and status:
        return {
            'data_min': datamin,
            'data_max': add_hours(datamax),
            'status': status,
            'codusuario': codusuario,
            'limit': limit,
            'offset': offset
        }
    elif codusuario:
        return {
            'data_min': datamin,
            'data_max': add_hours(datamax),
            'codusuario': codusuario,
            'limit': limit,
            'offset': offset
        }
    elif status:
        return {
            'data_min': datamin,
            'data_max': add_hours(datamax),
            'status': status,
            'limit': limit,
            'offset': offset
    }
    return {
        'data_min': datamin,
        'data_max': add_hours(datamax),
        'limit': limit,
        'offset': offset
    }


consulta_sem_codusuario_com_status = " SELECT * FROM cliente WHERE (datavis >= ? and datavis <= ?)\
                        and status = ? LIMIT ? OFFSET ?"
consulta_com_codusuario_sem_status = " SELECT * FROM cliente WHERE (datavis >= ? and datavis <= ?)\
                        and codusuario = ? LIMIT ? OFFSET ?"
consulta_com_codusuario_com_status = " SELECT * FROM cliente WHERE (datavis >=? and datavis <=?)\
                        and status = ? and codusuario = ? LIMIT ? OFFSET ?"
consulta_geral = " SELECT * FROM cliente WHERE (datavis >= ? and datavis <= ?)\
                        LIMIT ? OFFSET ?"
