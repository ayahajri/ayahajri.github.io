from flask import Flask, render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging
from dotenv import load_dotenv

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Charger les variables d'environnement
load_dotenv()

app = Flask(__name__)

# Configuration de l'email
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
RECIPIENT_EMAIL = os.getenv('RECIPIENT_EMAIL', 'hajriaya16@gmail.com')

print("EMAIL_ADDRESS =", EMAIL_ADDRESS)
print("EMAIL_PASSWORD =", EMAIL_PASSWORD)

@app.route('/')
def portfolio():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')
    
    if not all([name, email, subject, message]):
        return jsonify({'success': False, 'message': 'Tous les champs sont obligatoires'}), 400
    
    try:
        # Créer le message email
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = f"Portfolio Contact: {subject}"
        
        body = f"""
        Nouveau message de votre portfolio:
        
        Nom: {name}
        Email: {email}
        Sujet: {subject}
        
        Message:
        {message}
        """
        msg.attach(MIMEText(body, 'plain'))
        
        # Envoyer l'email avec gestion d'erreur améliorée
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.ehlo()
                server.starttls()
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
                logging.info("Email envoyé avec succès")
                
        except smtplib.SMTPAuthenticationError:
            logging.error("Échec d'authentification SMTP")
            return jsonify({
                'success': False,
                'message': 'Échec d\'authentification. Vérifiez vos identifiants email.'
            }), 401
            
        except Exception as e:
            logging.error(f"Erreur SMTP: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Erreur de connexion au serveur SMTP: {str(e)}'
            }), 503
        
        return jsonify({'success': True, 'message': 'Message envoyé avec succès!'})
    
    except Exception as e:
        logging.error(f"Erreur générale: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Erreur inattendue: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)