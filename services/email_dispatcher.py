# services/email_dispatcher.py
import os
import random

def executar_disparo_email(ref_alvo, nome_alvo, foto_alvo, recomendacoes_front):
    print(f"\n[EMAIL DISPATCHER] Iniciando segmentação e montagem dinâmica para: {nome_alvo}")
    
    # Simulação de público impactado (Mock Data para compliance com a LGPD na banca)
    qtd_clientes_mock = random.randint(150, 850)
    
    # Filtra rigorosamente as TOP 5 recomendações vindas diretamente da tela do frontend
    top_5_recs = recomendacoes_front[:5]

    # Construção dinâmica da vitrine de e-mail baseada nos produtos da página
    html_cards = ""
    for rec in top_5_recs:
        nome_produto = rec.get('nome', 'Lançamento Sonho dos Pés')
        preco_produto = rec.get('preco', 'Consulte no site')
        foto_produto = rec.get('foto', '')

        html_cards += f"""
        <div style="display: inline-block; width: 170px; margin: 8px; background: #ffffff; border-radius: 12px; border: 1px solid #f3f4f6; overflow: hidden; vertical-align: top; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
            <img src="{foto_produto}" style="width: 100%; height: 160px; object-fit: cover; background: #fafafa;" alt="{nome_produto}">
            <div style="padding: 12px; font-family: sans-serif;">
                <h4 style="font-size: 12px; color: #374151; margin: 0 0 6px 0; height: 32px; overflow: hidden; line-height: 1.3; font-weight: 600;">{nome_produto}</h4>
                <p style="font-size: 14px; font-weight: 700; color: #E6007E; margin: 0 0 10px 0;">{preco_produto}</p>
                <a href="#" style="display: block; background: #E6007E; color: #ffffff; text-decoration: none; padding: 7px 0; border-radius: 6px; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Quero Este</a>
            </div>
        </div>
        """

    # Template final de e-mail com linguagem 100% focada no cliente final
    html_email = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Sonho dos Pés | Escolhas Especiais para Você</title>
    </head>
    <body style="margin: 0; padding: 0; background-color: #f4f4f5; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f4f4f5; padding: 30px 10px;">
            <tr>
                <td align="center">
                    <table width="600" cellpadding="0" cellspacing="0" border="0" style="background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 30px rgba(0,0,0,0.04); border: 1px solid #e5e7eb;">
                        
                        <tr>
                            <td align="center" style="padding: 35px; background: linear-gradient(135deg, #E6007E, #ff3399);">
                                <h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 700; letter-spacing: 3px; text-transform: uppercase;">SONHO DOS PÉS</h1>
                                <p style="color: rgba(255,255,255,0.85); margin: 5px 0 0 0; font-size: 11px; letter-spacing: 1px; text-transform: uppercase;">Novidades Exclusivas para o seu Estilo</p>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 40px 35px 20px; text-align: center;">
                                <h2 style="color: #111827; font-size: 22px; font-weight: 700; margin: 0 0 12px 0;">Vimos que você amou este produto!</h2>
                                <p style="color: #4b5563; font-size: 15px; line-height: 1.6; margin: 0 0 25px 0;">
                                    Preparamos uma seleção super especial baseada na sua última escolha. Olhe só o que combina perfeitamente com o seu novo calçado:
                                </p>
                                
                                <div style="background: #fafafa; border: 1px solid #f3f4f6; border-radius: 12px; padding: 15px; display: inline-block; width: 230px; margin-bottom: 10px;">
                                    <img src="{foto_alvo}" style="width: 100%; height: 190px; object-fit: cover; border-radius: 8px; border: 1px solid #e5e7eb;" alt="Seu Calçado">
                                    <h3 style="font-size: 13px; color: #374151; margin: 12px 0 0 0; text-transform: uppercase; font-weight: 600; line-height: 1.4;">{nome_alvo}</h3>
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 0 35px;">
                                <div style="border-top: 2px dashed #e5e7eb; height: 1px; width: 100%;"></div>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding: 30px 15px 20px; text-align: center;">
                                <h3 style="color: #E6007E; font-size: 16px; font-weight: 700; margin: 0 0 20px 0; text-transform: uppercase; letter-spacing: 0.5px;">Você também vai amar combinar com:</h3>
                                
                                <div style="font-size: 0; text-align: center;">
                                    {html_cards}
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td align="center" style="padding: 35px; background-color: #fff0f6; border-top: 1px solid #ffe3ef; border-bottom-left-radius: 16px; border-bottom-right-radius: 16px;">
                                <p style="color: #1f2937; font-size: 16px; font-weight: 600; margin: 0 0 12px 0;">Para deixar seu look completo, preparamos um presente:</p>
                                <div style="display: inline-block; border: 2px dashed #E6007E; padding: 12px 35px; border-radius: 8px; background-color: #ffffff; box-shadow: 0 4px 10px rgba(230,0,126,0.05);">
                                    <span style="font-size: 26px; font-weight: 800; color: #E6007E; letter-spacing: 3px;">VOLTE20</span>
                                </div>
                                <p style="color: #6b7280; font-size: 12px; margin: 15px 0 0 0; font-weight: 500;">Use o cupom acima para garantir 20% OFF em sua próxima compra online.</p>
                            </td>
                        </tr>

                    </table>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    # Gravação do arquivo físico que alimenta a aba de visualização
    caminho_preview = os.path.join("frontend", "preview_campanha.html")
    with open(caminho_preview, "w", encoding="utf-8") as f:
        f.write(html_email)
        
    print(f"[EMAIL DISPATCHER] Arquivo dinâmico gravado em {caminho_preview}")
    return {"success": True, "impacted": qtd_clientes_mock, "preview_url": "/preview_campanha.html"}