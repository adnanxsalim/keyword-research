import requests
import xml.etree.ElementTree as ET

class AutoCompleteExplorer:
    def GetAutoCompleteResults(self, userInput, countryCode):
        results = []
        googleAutoCompleteUrl = f"http://suggestqueries.google.com/complete/search?output=toolbar&gl={countryCode}&q={userInput}"

        result = requests.get(googleAutoCompleteUrl)
        tree = ET.ElementTree(ET.fromstring(result.content))
        root = tree.getroot()
        for suggestion in root.findall('CompleteSuggestion'):
            suggestion_text = suggestion.find('suggestion').attrib.get('data')
            results.append(suggestion_text)

        return results

if __name__ == "__main__":
    userInput = input("Enter a Keyword: ")
    countryCode = input("Enter your Country Code (e.g., us, uk, ca): ")
    autoCompleteObj = AutoCompleteExplorer()
    autoCompleteResults = autoCompleteObj.GetAutoCompleteResults(userInput, countryCode)

    if autoCompleteResults:
        print("AutoComplete Suggestions:")
        for index, result in enumerate(autoCompleteResults, start=1):
            print(f"{index}. {result}")
    else:
        print("No AutoComplete suggestions found.")

    print("Done")