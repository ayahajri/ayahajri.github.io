import smtplib

email_address = "hajriaya16@gmail.com"
email_password = "zmeyjqrmkypjdsll"  # ton mot de passe d'application

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(email_address, email_password)
        print("✅ Connexion réussie à Gmail SMTP.")
except smtplib.SMTPAuthenticationError as e:
    print("❌ Erreur d'authentification SMTP :", e.smtp_error.decode())
except Exception as e:
    print("❌ Erreur SMTP :", str(e))
