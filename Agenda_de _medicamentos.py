import tkinter as tk
import time
import threading
from tkinter import messagebox
import schedule
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações de e-mail
smtp_server = 'smtp.seuservidor.com'
smtp_port = 587  # Porta SMTP padrão para TLS
email_usuario = 'seu_email@gmail.com'
senha = 'sua_senha'

# Função para enviar e-mail
def enviar_email(destinatario, assunto, mensagem):
    try:
        servidor_smtp = smtplib.SMTP(smtp_server, smtp_port)
        servidor_smtp.starttls()
        servidor_smtp.login(email_usuario, senha)

        email = MIMEMultipart()
        email['From'] = email_usuario
        email['To'] = destinatario
        email['Subject'] = assunto
        email.attach(MIMEText(mensagem, 'plain'))

        servidor_smtp.sendmail(email_usuario, destinatario, email.as_string())
        servidor_smtp.quit()
        print('E-mail enviado com sucesso!')
    except Exception as e:
        print('Ocorreu um erro ao enviar o e-mail:', str(e))

# Função para enviar lembrete por e-mail e exibir na interface gráfica
def enviar_lembrete_email_e_interface(nome, medicamento):
    assunto = f"Lembrete para {nome}"
    mensagem = f"Olá, {nome}! É hora de tomar o medicamento: {medicamento} Dosagem: {dosagem}"
    enviar_email(destinatario, assunto, mensagem)
    messagebox.showinfo("Lembrete", mensagem)


# Adicionar Registro
def adicionar_registro():
    nome = entry_nome.get()
    data = entry_data.get()
    horario = entry_horario.get()
    medicamento = entry_medicamento.get()
    dosagem = entry_dosagem.get()
    destinatario = entry_email.get()

    if nome and data and horario and medicamento and dosagem and destinatario:
        # Exibir os dados inseridos na caixa de texto
        registro_text.insert(tk.END, f"Nome: {nome}, Data: {data}, Horário: {horario}, Medicamento: {medicamento}, Dosagem: {dosagem}, Email: {destinatario}\n")

        # Agendar o lembrete para o horário especificado
        agendar_lembrete(nome, data, horario, medicamento, dosagem)

        # Limpar os campos de entrada
        entry_nome.delete(0, tk.END)
        entry_data.delete(0, tk.END)
        entry_horario.delete(0, tk.END)
        entry_medicamento.delete(0, tk.END)
        entry_dosagem.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    else:
        messagebox.showinfo("Erro", "Por favor, preencha todos os campos.")

def agendar_lembrete(nome, data, horario, medicamento,dosagem):
    # Converter a data e horário em segundos desde a época (01/01/1970)
    data_hora_str = f"{data} {horario}"
    data_hora = time.mktime(time.strptime(data_hora_str, "%d/%m/%Y %H:%M"))

    # Obter o tempo atual em segundos desde a época
    tempo_atual = time.time()

    # Calcular a diferença de tempo para o lembrete
    diferenca_tempo = data_hora - tempo_atual

    if diferenca_tempo <= 0:
        messagebox.showinfo("Erro", "A data e hora especificadas já passaram.")
    else:
        # Agendar o lembrete usando a biblioteca 'schedule'
        schedule.every(diferenca_tempo).seconds.do(enviar_lembrete, nome, medicamento, dosagem)
        messagebox.showinfo("Sucesso", "Lembrete agendado com sucesso!")

def enviar_lembrete(nome, medicamento, dosagem):
    # Esta função será chamada quando for hora de enviar o lembrete
    messagebox.showinfo("Lembrete", f"Olá, {nome}! É hora de tomar o medicamento: {medicamento}, Dosagem: {dosagem}")

# Configurar a janela principal
root = tk.Tk()
root.title("Agenda de Medicamentos")
root.geometry("900x600")

# Criar rótulos e campos de entrada
tk.Label(root, text="Nome:").pack()
entry_nome = tk.Entry(root)
entry_nome.pack()

tk.Label(root, text="Data (DD/MM/AAAA):").pack()
entry_data = tk.Entry(root)
entry_data.pack()

tk.Label(root, text="Horário (HH:MM):").pack()
entry_horario = tk.Entry(root)
entry_horario.pack()

tk.Label(root, text="Medicamento:").pack()
entry_medicamento = tk.Entry(root)
entry_medicamento.pack()

tk.Label(root, text="Dosagem:").pack()
entry_dosagem = tk.Entry(root)
entry_dosagem.pack()

tk.Label(root, text="E-mail (destinatário):").pack()
entry_email = tk.Entry(root)
entry_email.pack()

# Botão para adicionar registro
adicionar_button = tk.Button(root, text="Adicionar Registro", command=adicionar_registro)
adicionar_button.pack()

# Caixa de texto para exibir registros
registro_text = tk.Text(root, height=20, width=110)
registro_text.pack()

# Iniciar o agendamento em segundo plano
def agendamento_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Iniciar a thread para executar o agendamento em segundo plano
agendamento_thread = threading.Thread(target=agendamento_thread)
agendamento_thread.start()

# Iniciar a interface gráfica
root.mainloop()