from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import Medico, Paziente, NotaDiario
from django.contrib import messages
from django.contrib.auth import logout
from datetime import date
from llama_cpp import Llama
import logging
from django.shortcuts import get_object_or_404


logger = logging.getLogger(__name__)
model_path = "./models/mistral/mistral-7b-openorca.Q8_0.gguf"
llama_model = Llama(model_path=model_path, n_ctx=2048)



def home(request):
    return render(request, 'SoulDiaryConnectApp/home.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        medico = Medico.objects.filter(email=email, passwd=password).first()
        paziente = Paziente.objects.filter(email=email, passwd=password).first()

        if medico:
            request.session['user_type'] = 'medico'
            request.session['user_id'] = medico.codice_identificativo
            next_url = request.GET.get('next', 'medico_home')
            print(f"Redirecting to: {next_url}")
            return redirect(next_url)
        elif paziente:
            request.session['user_type'] = 'paziente'
            request.session['user_id'] = paziente.codice_fiscale
            next_url = request.GET.get('next', 'paziente_home')
            print(f"Redirecting to: {next_url}")
            return redirect(next_url)
        else:
            print("Login fallito")
            messages.error(request, 'Email o password non validi.')

    return render(request, 'SoulDiaryConnectApp/login.html')

def register_view(request):
    if request.method == 'POST':
        user_type = request.POST['user_type']  # medico o paziente

        # Dettagli comuni
        nome = request.POST['nome']
        cognome = request.POST['cognome']
        email = request.POST['email']
        passwd = request.POST['passwd']

        if user_type == 'medico':
            # Dettagli specifici per il medico
            codice_identificativo = request.POST['codice_identificativo']
            indirizzo_studio = request.POST['indirizzo_studio']
            citta = request.POST['citta']
            numero_civico = request.POST['numero_civico']
            numero_telefono_studio = request.POST.get('numero_telefono_studio')
            numero_telefono_cellulare = request.POST.get('numero_telefono_cellulare')

            # Creazione del medico
            Medico.objects.create(
                codice_identificativo=codice_identificativo,
                nome=nome,
                cognome=cognome,
                indirizzo_studio=indirizzo_studio,
                citta=citta,
                numero_civico=numero_civico,
                numero_telefono_studio=numero_telefono_studio,
                numero_telefono_cellulare=numero_telefono_cellulare,
                email=email,
                passwd=passwd,
            )
        elif user_type == 'paziente':
            # Dettagli specifici per il paziente
            codice_fiscale = request.POST['codice_fiscale']
            data_di_nascita = request.POST['data_di_nascita']
            med = request.POST['med']

            # Creazione del paziente
            Paziente.objects.create(
                codice_fiscale=codice_fiscale,
                nome=nome,
                cognome=cognome,
                data_di_nascita=data_di_nascita,
                med=Medico.objects.get(codice_identificativo=med),
                email=email,
                passwd=passwd,
            )

        messages.success(request, 'Registrazione completata con successo!')
        return redirect('login')

    return render(request, 'SoulDiaryConnectApp/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def medico_home(request):
    if request.session.get('user_type') != 'medico':
        return redirect('/login/')

    medico_id = request.session.get('user_id')
    medico = get_object_or_404(Medico, codice_identificativo=medico_id)

    # Lista dei pazienti
    pazienti = Paziente.objects.filter(med=medico)

    # Paziente selezionato
    paziente_id = request.GET.get('paziente_id')
    paziente_selezionato = Paziente.objects.filter(codice_fiscale=paziente_id).first()

    # Note del paziente selezionato
    note_diario = NotaDiario.objects.filter(paz=paziente_selezionato) if paziente_selezionato else None

    return render(request, 'SoulDiaryConnectApp/medico_home.html', {
        'medico': medico,
        'pazienti': pazienti,
        'paziente_selezionato': paziente_selezionato,
        'note_diario': note_diario,
    })



# Funzione per la generazione di frasi
def genera_frasi_di_supporto(testo):
    print("generazione frasi supporto")
    try:
        #result = llama_model(f"Genera un feedback di supporto al seguente testo: {testo}", max_tokens=200)
        #result = llama_model(f"Generate a support feedback about this text: {testo}", max_tokens=70)
        #result = llama_model(f"Provide a supportive and motivational message for the following text: {testo}. The response should be empathetic, encouraging, and helpful.", max_tokens=70)
        #prompt = f"The goal is to provide an empathetic and supportive feedback. The feedback should express empathy for the emotions described. Provide motivation and encouragement; offer practical advice to improve the situation. The text is: {testo}"
        prompt = f"""
        You are a supportive assistant. Use the following example to craft your response.

        Example:
        Text: "I failed my exam and feel like giving up."
        Response: "I'm so sorry to hear about your exam. It's okay to feel disappointed, but this doesn't define your worth. Consider revising your study strategy and asking for help. You've got this!"

        Now, respond to the following text:
        {testo}
        """

        result = llama_model(prompt, max_tokens=150)
        print(result['choices'][0]['text'].strip())
        return result['choices'][0]['text'].strip()
    except Exception as e:
        return f"Errore durante la generazione: {e}"


def genera_frasi_cliniche(testo, medico):
    print("generazione commenti clinici")
    """
    Genera un testo clinico basato sui parametri specifici del medico.

    :param testo: Il testo fornito dal paziente.
    :param medico: L'oggetto medico contenente i parametri di personalizzazione.
    :return: Il testo generato o un messaggio di errore.
    """
    try:
        # Determina i parametri dal medico
        tipo_nota = medico.tipo_nota  # True per "strutturato", False per "non strutturato"
        lunghezza_nota = medico.lunghezza_nota  # True per "lungo", False per "breve"
        tipo_parametri = medico.tipo_parametri.split(".:;!") if medico.tipo_parametri else []
        testo_parametri = medico.testo_parametri.split(".:;!") if medico.testo_parametri else []

        # Determina il max_tokens in base alla lunghezza_nota
        max_tokens = 250 if lunghezza_nota else 150

        if tipo_nota:
            # Genera il prompt strutturato con parametri
            parametri_strutturati = "\n".join(
                [f"{tipo}: {testo}" for tipo, testo in zip(tipo_parametri, testo_parametri)]
            )

            prompt = f"""
                You are a psychotherapist specializing in CBT. Analyze the following text and provide a clinical assessment.

                Example:
                Text: "Today I failed my exam and feel like giving up."
                Response: 
                {parametri_strutturati}
                
                Parameters:
                {tipo_parametri}

                Now analyze this text:
                {testo}

                Respond in the format of the example response:
                """
        else:
            # Genera il prompt non strutturato
            prompt = f"""
                You are a psychotherapist specializing in CBT. Analyze the following text and provide a clinical assessment. The text is: {testo}
                """

        # Genera il risultato usando il modello
        result = llama_model(prompt, max_tokens=max_tokens)
        print(result['choices'][0]['text'].strip())
        return result['choices'][0]['text'].strip()

    except Exception as e:
        return f"Errore durante la generazione: {e}"


def paziente_home(request):
    if request.session.get('user_type') != 'paziente':
        return redirect('/login/')

    paziente_id = request.session.get('user_id')
    if not paziente_id:
        return redirect('/login/')

    paziente = Paziente.objects.get(codice_fiscale=paziente_id)
    #print(f"Paziente trovato: {paziente.nome} {paziente.cognome}")
    #print(f"Medico associato (ID): {paziente.med}")

    try:
        medico = paziente.med
        #print(f"Medico trovato: {medico.nome} {medico.cognome}")
    except Medico.DoesNotExist:
        medico = None
        print("Nessun medico trovato associato a questo paziente.")

    if request.method == 'POST':
        testo_paziente = request.POST.get('desc')
        generate_response_flag = request.POST.get('generateResponse') == 'on'  # Checkbox per generare frasi di supporto
        testo_supporto = ""
        testo_clinico = ""

        if testo_paziente:
            testo_supporto = genera_frasi_di_supporto(testo_paziente)

            # Genera il feedback clinico in base ai parametri del medico associato
            testo_clinico = genera_frasi_cliniche(testo_paziente, medico)

            # Crea una nuova nota di diario
            NotaDiario.objects.create(
                paz=paziente,
                testo_paziente=testo_paziente,
                testo_supporto=testo_supporto,
                testo_clico=testo_clinico,
                data_nota=date.today()
            )

    note_diario = NotaDiario.objects.filter(paz=paziente)

    return render(request, 'SoulDiaryConnectApp/paziente_home.html', {
        'paziente': paziente,
        'note_diario': note_diario,
        'medico' : medico,
    })


def modifica_testo_medico(request, nota_id):
    if request.method == 'POST':
        nota = get_object_or_404(NotaDiario, id=nota_id)
        testo_medico = request.POST.get('testo_medico', '').strip()
        nota.testo_medico = testo_medico
        nota.save()
        return redirect(f'/medico/home/?paziente_id={nota.paz.codice_fiscale}')

def personalizza_generazione(request):
    if request.session.get('user_type') != 'medico':
        return redirect('/login/')

    medico_id = request.session.get('user_id')
    medico = Medico.objects.get(codice_identificativo=medico_id)

    if request.method == 'POST':
        # Tipo di Nota
        tipo_nota = request.POST.get('tipo_nota')
        medico.tipo_nota = True if tipo_nota == 'strutturato' else False

        # Lunghezza della Nota
        lunghezza_nota = request.POST.get('lunghezza_nota')
        medico.lunghezza_nota = True if lunghezza_nota == 'lungo' else False

        # Concatenazione di tipo_parametri e testo_parametri
        tipo_parametri = request.POST.getlist('tipo_parametri')
        testo_parametri = request.POST.getlist('testo_parametri')
        medico.tipo_parametri = ".:;!".join(tipo_parametri)
        medico.testo_parametri = ".:;!".join(testo_parametri)

        medico.save()
        return redirect('medico_home')

    # Suddivide i parametri già salvati in liste per visualizzarli nella tabella
    tipo_parametri = medico.tipo_parametri.split(".:;!") if medico.tipo_parametri else []
    testo_parametri = medico.testo_parametri.split(".:;!") if medico.testo_parametri else []

    return render(request, 'SoulDiaryConnectApp/personalizza_generazione.html', {
        'medico': medico,
        'tipo_parametri': zip(tipo_parametri, testo_parametri),
    })
