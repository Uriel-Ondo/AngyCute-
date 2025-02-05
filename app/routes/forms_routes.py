from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from wtforms.fields import EmailField
from flask_wtf.file import FileField, FileAllowed


class ConnexionForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Votre email"})
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()], render_kw={"placeholder": "Votre mot de passe"})
    submit = SubmitField('Se connecter')

class InscriptionForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Téléphone', validators=[DataRequired()])
    adresse = StringField('Adresse', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirmer_mot_de_passe = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('mot_de_passe', message='Les mots de passe doivent correspondre.')])
    submit = SubmitField("S'inscrire")

class MotDePasseOublieForm(FlaskForm):
    email = StringField('Adresse email', validators=[DataRequired(), Email()])
    submit = SubmitField("Envoyer un email")
    
class ReinitialisationMotDePasseForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField(
        'Nouveau mot de passe',
        validators=[DataRequired(), Length(min=6, message="Le mot de passe doit contenir au moins 6 caractères")]
    )
    confirmer_mot_de_passe = PasswordField(
        'Confirmer le mot de passe',
        validators=[DataRequired(), EqualTo('mot_de_passe', message="Les mots de passe ne correspondent pas")]
    )
    submit = SubmitField("Réinitialiser")
    
class ContactForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    sujet = StringField('Sujet', validators=[DataRequired(), Length(min=2, max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Envoyer")
