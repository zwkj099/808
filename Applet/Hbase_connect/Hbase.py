
def HbaseData(sim_card):

    import happybase

    conn = happybase.Connection('192.168.24.122',9090)
    conn.open()
    table = conn.table('TEST:POSITIONAL')

    info = table.families()
    print info

    sub='substring:'+str(sim_card)

    query_str = "SingleColumnValueFilter ('0', 'SIM_CARD', =, '"+sub+"',true, false)"
    print query_str

    query = table.scan(filter=query_str,limit=1,include_timestamp=True,reverse=True)
    # query = table.scan(filter=query_str, row_start='67ff005aea154933b9aa38d8057bbbfa800000005cc55e9a',
    #                    include_timestamp=True)
    result = list(query)
    print result
    conn.close()
    return result


# reee = HbaseData('18876763277')
# print reee










