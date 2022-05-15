# urenPy
Een web-applicatie om je eigen uren te registreren.

# Functionaliteiten
De app heeft verschillende functionaliteiten ingebouwd. 
Alle gegevens die worden ingevoerd, worden vastgelegd in een SQLite3-database. 

* Entiteiten
  * Personen
  * Werkgevers
  * Contracten
  * Uren

Elke entiteit kan worden aangevuld en gemuteerd via de web-app.

Je kan vastleggen hoeveel vakantiedagen je per jaar wettelijk hebt. 

# To do
* add the uren-tab
* create reports
  * All hours in a crosstab (personen vs soort uren) per year/quarter/month
  * tab with simplified numbers per person (hoeveel vakantie-uren over dit jaar, ...)
* Use a WSGI Production server for flask


# How to use
Just run `python app.py` and the deploy-script will create an empty database-file named `urenPy.db`.

After that, the flask-app runs on http://0.0.0.0:8050/dash. 

# Example

![alt text](https://raw.githubusercontent.com/roytje88/urenPy/1cb40cecade18bd65892f97b1910f45f8ccbff58/example.png)
