- Förbered en separat dokumentationsfil som beskriver hur din applikation fungerar.
- Detta kan vara en `.pdf` eller en markdown-fil med namnet `Documentation` som skickas med i zip filen när du lämnar in projektet
- Din dokumentation bör innehålla följande

**Arkitektur**: Mitt program för personlig ekonomihantering är uppbyggt kring flera huvudklasser som samverkar för att hantera olika aspekter av användarens ekonomi.

- `UserAuth`: Denna klass hanterar användarautentisering. Den sparar och läser användardata från en JSON-fil (`users.json`). Klassen hanterar inloggning och registrering av användare.
    
- `Transaction`: Denna klass representerar en enskild transaktion, vare sig det är en inkomst eller utgift. Varje transaktion innefattar typ (inkomst/utgift), belopp, kategori och datum.
    
- `TransactionManager`: Ansvarar för att hantera en användares transaktioner. Den laddar och sparar transaktionsdata i användarens datafil (`{username}_data.json`) och kan lägga till nya transaktioner i användarens ekonomiska översikt.
    
- `BudgetManager`: Denna klass hanterar användarens budget. Den kan skapa, uppdatera och jämföra budgetar med faktiska utgifter, och även generera data för budgetjämförelser.
    
- `FinancialReport`: Ansvarig för att generera sammanfattningar av användarens ekonomi över olika tidsperioder (vecka, månad, år) och exportera dessa rapporter.
    
- `FinanceManagerApp`: Huvudklassen som kör programmet. Den hanterar användarinteraktioner, som att navigera i olika menyer och anropa rätt funktioner i andra klasser baserat på användarens val.
    

**Dataflöde**:

1. **Inmatning**: Användaren interagerar med programmet genom en serie menyer. De kan registrera sig, logga in, ange transaktioner (inkomster och utgifter), skapa budgetar, och begära rapporter.
    
2. **Lagring**: All användardata, inklusive login-information och transaktionsdata, lagras i JSON-filer. Varje användare har sin egen datafil (`{username}_data.json`), där deras transaktioner och budgetar sparas.
    
3. **Hantering**: När användaren begär det, läser programmet data från dessa filer. `TransactionManager` och `BudgetManager` klasserna hanterar denna data, antingen genom att uppdatera den med nya transaktioner eller genom att använda befintlig data för att skapa budgetrapporter och ekonomiska sammanfattningar.
    
4. **Hämtning och Presentation**: När användaren begär rapporter eller budgetöversikter, samlar programmet relevant data och presenterar den antingen direkt i konsolen eller exporterar den till en fil, beroende på användarens val. Dataflödet är designat för att vara intuitivt och användarvänligt, samtidigt som det tillhandahåller en detaljerad översikt över användarens ekonomiska situation.


    - **Utmaningar och lösningar**: Diskutera eventuella betydande utmaningar som du ställdes inför och hur du löste dem. 

1. Det var svårt att få till det med veckor, månader och år och se till att allt stämde med användarens val. Men jag använde något som heter `datetime` i Python för att få ordning på datumen. Sedan gjorde jag så att programmet kunde välja ut transaktioner för den tidsperiod användaren ville ha, så att man kunde se sin ekonomi för just den tiden.
    
2. Att få programmet att spara rapporter på ett bra sätt var också klurigt. Jag ville se till att allt såg rätt ut när det sparades. Så jag jobbade mycket med att få ordning på hur datan skulle se ut och skrev funktioner som kunde skriva allt rätt i en fil. Nu kan programmet spara användarens ekonomi så man kan titta på den senare.
    
3. Jag ville också att man skulle kunna spara en kopia av sin ekonomi och kunna ladda tillbaka den om något hände. Det svåra här var att se till att inget blev fel om det redan fanns en fil med användarens data. Jag löste det genom att varna användaren om det kunde bli problem och förklarade hur man ska göra. Det här gör programmet säkrare och lättare att använda.
    
4. Jag ville att programmet skulle vara lätt att förstå och använda. Först var det inte så lätt att få alla funktioner att vara lätta att hitta. Men jag fixade det genom att göra menyn tydlig och ge bra instruktioner till användaren. Nu är det mycket enklare att använda programmet.

**Framtida förbättringar**: Beskriv potentiella förbättringar eller ytterligare funktioner som du kan implementera i framtiden. Export funktionerna, implementera bättre klass struktur för potentiella framtida utvecklingar av applikationen.

1. **Tidsram för Budgeten**: Jag vill lägga till en funktion där man kan se hur budgeten såg ut för tidigare månader. Just nu sätter man bara en budget och följer hur den används. Det vore bra att kunna jämföra och se över budgeten över tid.
    
2. **Bättre Hantering av Budget**: Jag behöver förbättra hur programmet hanterar och uppdaterar budgeten. När man skapar eller ändrar budgeten borde det finnas mer funktionalitet och flexibilitet.
    
3. **Verifiering av Backup**: Backup-funktionen borde förbättras. Jag tänker att det vore bra med någon sorts verifiering för att se till att backupen fungerar som den ska.
    
4. **Bättre Visualisering vid Export**: När man exporterar data från programmet vore det snyggt att ha en bättre visualisering. Kanske kan jag använda ett externt bibliotek för att skapa PDF-filer som visar ekonomin på ett tydligt sätt.
    
5. **Planering för Framtida Förbättringar**: Jag behöver tänka mer på hur programmet är uppbyggt. Stora ändringar kan behöva göras i framtiden när jag lägger till nya funktioner. Om jag redan nu förbereder klassstrukturen för framtida uppdateringar, kan jag undvika problem och göra det lättare att lägga till nya saker i programmet.