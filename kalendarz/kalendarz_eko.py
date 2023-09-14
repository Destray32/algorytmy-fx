import requests
import json
import datetime

#TODO:

class Kalendarz:
    def __init__(self, waluta):
        """
        Initializes a new instance of the Kalendarz class.

        Args:
        waluta (list): A list of currency codes to check on the calendar.
        """
        self.waluta = waluta
        self.daty = []
        self.daty_wstecz = []
        self.daty_po = []

    def PobierzDaty(self):
        """
        Retrieves dates from the calendar for the specified currencies.
        """
        response = requests.get("https://nfs.faireconomy.media/ff_calendar_thisweek.json?version=821cb1b2cef35a07ce66eae15f517645")
        data = response.json()

        filtered_data = [obj for obj in data if obj["country"] in self.waluta and obj["impact"] == "Low"]
        
        for obj in filtered_data:
            self.daty.append(obj["date"])

    
    def ZnajdzGodzineWstecz(self):
        """
        Finds the date and time one hour before each date in the daty list.
        """
        one_hour = datetime.timedelta(hours=1)
        for date in self.daty:
            date = datetime.datetime.fromisoformat(date)
            new_date = date - one_hour
            new_date = new_date.isoformat()
            self.daty_wstecz.append(new_date)

    def ZnajdzGodzinePo(self):
        """
        Finds the date and time one hour after each date in the daty list.
        """
        one_hour = datetime.timedelta(hours=1)
        for date in self.daty:
            date = datetime.datetime.fromisoformat(date)
            new_date = date + one_hour
            new_date = new_date.isoformat()
            self.daty_po.append(new_date)


    def CzyHighImpact(self, ile_godzin_wstecz):
        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=datetime.timezone.utc)
        eastern = datetime.timezone(datetime.timedelta(hours=-ile_godzin_wstecz), name="EST")
        eastern_time = now.astimezone(eastern)
        iso_time = eastern_time.strftime("%Y-%m-%dT%H:%M:%S+00:00")

        for data in self.daty_wstecz:
            if iso_time > data and iso_time < self.daty_po[self.daty_wstecz.index(data)]:
                return True
        return False
        

    def PobierzDatyWstecz(self):
        """
        Returns a list of dates and times one hour before each date in the daty list.
        """
        return self.daty_wstecz
    
    def PobierzDatyPo(self):
        """
        Returns a list of dates and times one hour after each date in the daty list.
        """
        return self.daty_po
    
    def PobierzDatyNormalne(self):
        return self.daty
    
    


