
import unicodedata
import json
import os
import csv
from datetime import datetime



def normalize(text):
    if not isinstance(text, str):
        return text
    text = text.strip().lower()
    nfkd = unicodedata.normalize('NFD', text)
    return ''.join(ch for ch in nfkd if unicodedata.category(ch) != 'Mn')


RESET = '\033[0m'
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
CYAN = '\033[36m'
BOLD = '\033[1m'


DEFAULT_QUESTIONS = [
    {'q': 'Qual é a capital do Brasil?', 'a': 'brasilia', 'disp': 'Brasília'},
    {'q': 'Quanto é 5 x 8?', 'a': '40'},
    {'q': 'Qual planeta é o maior do sistema solar?', 'a': 'jupiter', 'disp': 'Júpiter'},
    {'q': 'Em que ano o homem pisou na Lua?', 'a': '1969'},
    {'q': 'Qual é a linguagem de programação que estamos usando?', 'a': 'python', 'disp': 'Python'},
    {'q': 'Qual é o maior oceano do mundo?', 'a': 'pacifico', 'disp': 'Pacífico'},
    {'q': 'Em que país fica a Torre Eiffel?', 'a': 'franca', 'disp': 'França'},
    {'q': 'Quantos lados tem um triangulo?', 'a': '3'},
    {'q': 'Qual é o animal terrestre mais rápido?', 'a': 'guepardo', 'disp': 'Guepardo'},
    {'q': 'Em que ano terminou a Segunda Guerra Mundial?', 'a': '1945'},
    {'q': 'Qual é a moeda do Japão?', 'a': 'iene', 'disp': 'Iene'},
    {'q': 'Quantos minutos tem uma hora?', 'a': '60'},
    {'q': 'Qual é a cor resultante da mistura de azul e amarelo?', 'a': 'verde', 'disp': 'Verde'},
    {'q': 'Quantos ossos tem o corpo humano adulto (aprox.)?', 'a': '206'},
    {'q': 'Qual é o maior país do mundo em área?', 'a': 'russia', 'disp': 'Rússia'},
    {'q': 'Qual elemento químico tem símbolo O?', 'a': 'oxigenio', 'disp': 'Oxigênio'},
    {'q': 'Em que continente fica o Egito?', 'a': 'asia', 'disp': 'Ásia'},
    {'q': 'Qual o nome da famosa ópera de Georges Bizet sobre uma cigana?', 'a': 'carmen', 'disp': 'Carmen'},
    {'q': 'Quantos dentes permanentes tem um adulto (aprox.)?', 'a': '32'},
    {'q': 'Qual é o principal ingrediente do guacamole?', 'a': 'abacate', 'disp': 'Abacate'},
]



def load_questions(filename='questions.json'):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return DEFAULT_QUESTIONS.copy()


def save_questions(questions_list, filename='questions.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(questions_list, f, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False



def print_banner():
    print(CYAN + '=' * 40 + RESET)
    print(CYAN + BOLD + 'BEM-VINDO AO QUIZ DE CONHECIMENTO GERAL' + RESET)
    print(CYAN + BOLD + YELLOW + 'CRIADOR: MAYCON'.center(40) + RESET)
    print(CYAN + '=' * 40 + RESET)


def print_panel(questions_list):
    print(CYAN + '╔' + '═' * 58 + '╗' + RESET)
    print(CYAN + '║' + RESET + BOLD + YELLOW + ' PAINEL DE RESPOSTAS (CRIADOR)'.center(58) + RESET + CYAN + '║' + RESET)
    print(CYAN + '╠' + '═' * 58 + '╣' + RESET)
    for i, q in enumerate(questions_list, start=1):
        num = f'{i:2d}'
        ans = q.get('disp', q['a'])
        print(CYAN + '║' + RESET + f' {num}. ' + GREEN + f'{ans}'.ljust(50) + RESET + CYAN + '║' + RESET)
    print(CYAN + '╚' + '═' * 58 + '╝' + RESET)


def print_questions_and_answers(questions_list):
    print(CYAN + '╔' + '═' * 78 + '╗' + RESET)
    print(CYAN + '║' + RESET + BOLD + YELLOW + ' PERGUNTAS E RESPOSTAS (CRIADOR)'.center(78) + RESET + CYAN + '║' + RESET)
    print(CYAN + '╠' + '═' * 78 + '╣' + RESET)
    for i, q in enumerate(questions_list, start=1):
        num = f'{i:2d}'
        print(CYAN + '║' + RESET + f' {num}. ' + BLUE + f"{q['q']}".ljust(72) + RESET + CYAN + '║' + RESET)
        ans = q.get('disp', q['a'])
        print(CYAN + '║' + RESET + '     ' + GREEN + f'Resp.: {ans}'.ljust(72) + RESET + CYAN + '║' + RESET)
    print(CYAN + '╚' + '═' * 78 + '╝' + RESET)


def export_panel_to_file(filename, questions_list):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('PAINEL DE RESPOSTAS (CRIADOR)\n')
            f.write('=' * 40 + '\n')
            for i, q in enumerate(questions_list, start=1):
                ans = q.get('disp', q['a'])
                f.write(f"{i:2d}. {ans}\n")
        return True
    except Exception:
        return False


def generate_html_report(csvfile='resultados_quiz.csv', output='relatorio.html'):
    rows = []
    if not os.path.exists(csvfile):
        return False
    with open(csvfile, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for r in reader:
            if len(r) >= 4:
                rows.append(r)
    try:
        with open(output, 'w', encoding='utf-8') as f:
            f.write('<!doctype html>\n<html><head><meta charset="utf-8"><title>Relatório Quiz</title></head><body>\n')
            f.write('<h1>Relatório do Quiz</h1>\n')
            f.write('<table border="1" cellpadding="6" cellspacing="0">\n')
            f.write('<tr><th>Timestamp</th><th>Nome</th><th>Pontuação</th><th>Total</th></tr>\n')
            for r in rows:
                f.write(f'<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td></tr>\n')
            f.write('</table>\n')
            f.write('</body></html>')
        return True
    except Exception:
        return False


def save_result(name, score, total, filename='resultados_quiz.csv'):
    try:
        linha = f'{datetime.now().isoformat()},{name},{score},{total}\n'
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(linha)
    except Exception:
        pass


def show_stats(filename='resultados_quiz.csv'):
    if not os.path.exists(filename):
        return None
    total_runs = 0
    sum_scores = 0
    best = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 4:
                continue
            score = int(parts[2])
            total_runs += 1
            sum_scores += score
            if score > best:
                best = score
    if total_runs == 0:
        return None
    avg = sum_scores / total_runs
    return {'runs': total_runs, 'best': best, 'avg': avg}



def edit_questions_menu(questions):
  
    while True:
        print(CYAN + '\n--- Editar Perguntas ---' + RESET)
        print('1) Listar perguntas')
        print('2) Adicionar pergunta')
        print('3) Editar pergunta existente')
        print('4) Remover pergunta')
        print('5) Salvar e voltar')
        print('6) Voltar sem salvar')
        choice = normalize(input(CYAN + 'Escolha (1-6): ' + RESET))
        if choice == '1':
            for i, q in enumerate(questions, start=1):
                print(f"{i}. {q['q']} -> {q.get('disp', q['a'])}")
        elif choice == '2':
            qtext = input('Texto da pergunta: ')
            atext = normalize(input('Resposta (sem acento, minúscula): '))
            dtext = input('Resposta exibida (opcional): ')
            entry = {'q': qtext, 'a': atext}
            if dtext:
                entry['disp'] = dtext
            questions.append(entry)
            print(GREEN + 'Pergunta adicionada.' + RESET)
        elif choice == '3':
            idx = input('Número da pergunta a editar: ')
            if not idx.isdigit() or int(idx) < 1 or int(idx) > len(questions):
                print(YELLOW + 'Índice inválido.' + RESET)
                continue
            i = int(idx) - 1
            print('Atual:', questions[i])
            qtext = input('Novo texto (enter para manter): ')
            if qtext:
                questions[i]['q'] = qtext
            atext = input('Nova resposta (leave para manter): ')
            if atext:
                questions[i]['a'] = normalize(atext)
            dtext = input('Nova resposta exibida (leave para manter): ')
            if dtext:
                questions[i]['disp'] = dtext
            print(GREEN + 'Pergunta atualizada.' + RESET)
        elif choice == '4':
            idx = input('Número da pergunta a remover: ')
            if not idx.isdigit() or int(idx) < 1 or int(idx) > len(questions):
                print(YELLOW + 'Índice inválido.' + RESET)
                continue
            del questions[int(idx) - 1]
            print(GREEN + 'Pergunta removida.' + RESET)
        elif choice == '5':
            ok = save_questions(questions)
            if ok:
                print(GREEN + 'Perguntas salvas em questions.json' + RESET)
            else:
                print(RED + 'Erro ao salvar perguntas.' + RESET)
            break
        elif choice == '6':
            break
        else:
            print(YELLOW + 'Opção inválida.' + RESET)


def ask_retry_struct(qobj):
    print(BLUE + qobj['q'] + RESET)
    resp = normalize(input(YELLOW + 'Sua resposta: ' + RESET))
    if resp == qobj['a']:
        print(GREEN + 'Correto!' + RESET)
        print()
        return 1
    print(RED + 'Errado! Tente novamente.' + RESET)
    resp2 = normalize(input(YELLOW + 'Segunda chance: ' + RESET))
    if resp2 == qobj['a']:
        print(GREEN + 'Correto na segunda tentativa!' + RESET)
        print()
        return 1
    else:
        disp = qobj.get('disp', qobj['a'])
        print(RED + f'Errado! A resposta é {disp}' + RESET)
        print()
        return 0

def main():
    print_banner()
    nome = input(CYAN + 'Qual é o seu nome? ' + RESET)
    questions = load_questions()

    if normalize(nome) == 'maycon':
        print(GREEN + 'Seja bem-vindo criador' + RESET)
        while True:
            print(CYAN + '\n--- Painel do Criador ---' + RESET)
            print('1) Mostrar respostas (painel)')
            print('2) Mostrar perguntas e respostas (completas)')
            print('3) Exportar painel para arquivo')
            print('4) Ver estatísticas (resultados salvos)')
            print('5) Editar perguntas (adicionar/editar/excluir)')
            print('6) Gerar relatório HTML')
            print('7) Continuar para o quiz')
            choice = normalize(input(CYAN + 'Escolha uma opção (1-7): ' + RESET))
            if choice == '1':
                print_panel(questions)
            elif choice == '2':
                print_questions_and_answers(questions)
            elif choice == '3':
                ok = export_panel_to_file('painel_maycon.txt', questions)
                if ok:
                    print(GREEN + 'Painel exportado para painel_maycon.txt' + RESET)
                else:
                    print(RED + 'Erro ao exportar painel.' + RESET)
            elif choice == '4':
                stats = show_stats()
                if stats is None:
                    print(YELLOW + 'Nenhum resultado registrado ainda.' + RESET)
                else:
                    print(CYAN + f"Total execuções: {stats['runs']}, melhor: {stats['best']}, média: {stats['avg']:.2f}" + RESET)
            elif choice == '5':
                edit_questions_menu(questions)
            elif choice == '6':
                ok = generate_html_report()
                if ok:
                    print(GREEN + 'relatorio.html gerado.' + RESET)
                else:
                    print(RED + 'Erro ao gerar relatorio.' + RESET)
            elif choice == '7':
                break
            else:
                print(YELLOW + 'Opção inválida.' + RESET)
        print()
    else:
        print(f'Olá {nome}, vamos começar!\\n')

    pontos = 0
    for q in questions:
        pontos += ask_retry_struct(q)

    save_result(nome, pontos, len(questions))

    print(CYAN + '=' * 40 + RESET)
    print(YELLOW + f'Quiz finalizado, {nome}!' + RESET)
    print(YELLOW + f'Vc acertou {pontos} perguntas de {len(questions)}' + RESET)
    print(CYAN + '=' * 40 + RESET)


if __name__ == '__main__':
    main()

