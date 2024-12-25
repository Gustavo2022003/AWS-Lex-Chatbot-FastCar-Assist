def lexResponse(intent, slots):
    intentResponse = intentSelector(intent, slots)
    return {
        "phrase": intentResponse,
        "s3_audio": "S3Link"
    }

def intentSelector(intent, slots):
    if intent == "alugarCarro":
        nome = slots.get('nome', {}).get('value', {}).get('interpretedValue', 'Não especificado')
        email = slots.get('email', {}).get('value', {}).get('interpretedValue', 'Não especificado')
        modeloCarro = slots.get('modeloCarro', {}).get('value', {}).get('interpretedValue', 'Não especificado')
        
        if modeloCarro == 'luxo':
            carro =  slots.get('carrosLuxo', {}).get('value', {}).get('interpretedValue', 'Não especificado')

        if modeloCarro == 'esportivo':
            carro =  slots.get('carrosEsportivos', {}).get('value', {}).get('interpretedValue', 'Não especificado')

        if modeloCarro == 'confortavel':
            carro =  slots.get('carrosConfortaveis', {}).get('value', {}).get('interpretedValue', 'Não especificado')

        if modeloCarro == 'economico':
            carro =  slots.get('carrosEconomicos', {}).get('value', {}).get('interpretedValue', 'Não especificado')

        cidade = slots.get('cidade', {}).get('value', {}).get('interpretedValue', 'Não especificado')
        horario = slots.get('horario', {}).get('value', {}).get('interpretedValue', 'Não especificado')
        qtdeDias = slots.get('qtdeDias', {}).get('value', {}).get('interpretedValue', 'Não especificado')

        return f'Muito obrigado, {nome}! Sua reserva para o aluguel de: {carro}, retirado em {cidade}, às {horario} horas, por {qtdeDias} dias foi efetuada com sucesso!'

    return 0