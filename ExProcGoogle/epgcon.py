from ExProcGoogle import ep_gauth
from googleapiclient.discovery import build

# returns a string with PhoneNumer,E-mail,Company and Note of the queried name in the Google Contacts
def get_contact_info(name: str) -> str:
    creds = ep_gauth.main()
    service = build("people", "v1", credentials=creds)
    results = (
        service.people()
        .searchContacts(
            pageSize=30,
            query=name,
            readMask="biographies,emailAddresses,phoneNumbers,organizations",
        )
        .execute()
    )
    result = " "

    if results.get("results"):
        quer = results["results"]
        for person in quer:
            header = person.get("person", [])
            result += "\n" + "This is the person found:" + "\n"
            if header:
                if header.get("phoneNumbers") is not None:
                    result += "Cell: " + header.get("phoneNumbers")[0]["value"]
                else:
                    result += "No Cell found"
                if header.get("emailAddresses") is not None:
                    result += ", Mail: " + header.get("emailAddresses")[0]["value"]
                else:
                    result += ", No Mail found"
                if header.get("organizations") is not None:
                    result += ", Company: " + header.get("organizations")[0]["name"]
                else:
                    result += ", No Company found"
                if header.get("biographies") is not None:
                    result += ", Note: " + header.get("biographies")[0]["value"]
                else:
                    result += ", No Bio found"

            else:
                result += "The person does not have content "
        return result
    else:
        result = "Sorry I could not find a person under that Name."
        return result

