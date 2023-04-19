# -*- coding: utf-8 -*-
"""
Library to transform data stored as Standard Audit Files - Tax (SAF-T) files to Pandas DataFrame.
Currently only supports the Norwegian SAF-T specification. The code is based on internal tools from
the Norwegian Tax Authority.
"""
from pathlib import Path
from typing import Tuple

from bs4 import BeautifulSoup
import pandas as pd



def find_organisation_number(soup: BeautifulSoup) -> str:
    '''Helper function that receives a "soup" from parsing the SAF-T, and extracts
    the company's registration number (as a string)'''
    
    namespaces={'n1': 'urn:StandardAuditFile-Taxation-Financial:NO'}
    orgnr = soup.select('n1|Header > n1|Company > n1|RegistrationNumber', namespaces=namespaces)

    if len(orgnr) != 1:
        return "dummyorgnr"
#        raise() # TODO: Add exception if there are either none or more than one organisation number identifying Company
    else:
        orgnr = orgnr[0].string

    return orgnr


def accounts2df(path: Path) -> Tuple[pd.DataFrame, str]:
    '''Reads a SAF-T file and extracts all the accounts listed in the elements <MasterFiles>, and
    adds them to a pandas DataFrame. The return value is a tuple that includes the dataframe, and
    a string that holds the organisation number that identifies the company. The latter is taken
    from the element Header>Company>RegistrationNumber (namespace omitted for brevity)'''

    with open(path, mode='r') as file:
        soup = BeautifulSoup(file, "xml")    

    orgnr = find_organisation_number(soup)

    MasterFiles = soup.find_all('MasterFiles')

    accountsdict = {}

    n = 0
    for f in MasterFiles:
        for account in f.find_all('Account'):
            n += 1
            input = {}
            for child in account.children:
                if child != '\n' and child.is_empty_element == False:
                    input[str(child.name)] = child.contents[0]
            accountsdict[str(n)] = input
    accounts = pd.DataFrame.from_dict(accountsdict, orient = 'index')

    return (accounts, orgnr)


def gle2df(file: str) -> Tuple[pd.DataFrame, str]:
    '''Reads a SAF-T file (either name/path of a file or the xml-content) and extracts
    all the General Ledger Entries from the elements
    <GeneralLedgerEntries>, and adds them to a pandas Dataframe. The return value is a 
    tuple that includes the dataframe, and a string that holds the organisation number
    that identifies the company. The latter is taken from the element
    Header>Company>RegistrationNumber'''

    soup = BeautifulSoup(file, "xml")

    # First, extract orgnr from the file
    orgnr = find_organisation_number(soup)

    # Second, get the mapping between AccountID and StandardAccountID
    MasterFiles = soup.find_all('MasterFiles')

    accountsdict = {}

    n = 0
    for f in MasterFiles:
        for account in f.find_all('Account'):
            n += 1
            input = {}
            for child in account.children:
                if child != '\n' and child.is_empty_element == False:
                    input[str(child.name)] = child.contents[0]
            accountsdict[str(n)] = input

    accounts = pd.DataFrame.from_dict(accountsdict, orient = 'index')

    # Check that AccountID is unique, and set it as index
    if not accounts['AccountID'].is_unique:
        raise ValueError("AccountID is not unique in MasterFiles")
    
    accounts.set_index('AccountID', inplace=True)

    # Third, get the General Ledger Entries, and map them to the StandardAccountID
    GLE = soup.find_all('GeneralLedgerEntries')

    linedict = {}
    n = 0
    for g in GLE:
        for transaction in g.find_all('Transaction'):
            input = {}
            for child in transaction.children:
                if child != '\n' and child.is_empty_element == False:
                    input[str(child.name)] = child.contents[0]
            for line in transaction.find_all('Line'):
                n += 1
                inputline = input.copy()
                for child in line.children:
                    if child != '\n' and child.is_empty_element == False:
                        if child.name == 'Analysis':
                            for c in child.children:
                                inputline[str(c.name)] = child.contents[0]
                        elif child.name == 'DebitAmount' or child.name == 'CreditAmount':
                            inputline[child.name] = child.Amount.string
                        elif child.name == 'TaxInformation':
                            for c in child.children:
                                inputline[c.name] = c.string
                        elif child.name == 'AccountID':
                            inputline[child.name] = child.string
                            inputline['StandardAccountID'] = accounts.loc[child.string]['StandardAccountID']
                        else:
                            inputline[str(child.name)] = child.contents[0]
                linedict[str(n)] = {key: str(value) for (key, value) in inputline.items()}
    lines = pd.DataFrame.from_dict(linedict, orient = 'index')

    if not (lines['StandardAccountID'].str.match(r'^\d{4}').all() or lines['StandardAccountID'].str.match(r'^\d{2}').all()):
        raise ValueError("StandardAccountID either missing for some transactions, or wrong format (should be 4 or 2 digits)")

    lines = lines.astype(dtype={
     # valg av datatype pr felt bør verifiseres av noen ...
#    'Transaction.Transaction': str,
#    'Transaction.TransactionID': str,
    'Period': int,
    'PeriodYear': int,
    'TransactionDate': 'datetime64',
#    'TransactionType': 'category',
#    'Transaction.Description': str,
    'SystemEntryDate': 'datetime64',
    'GLPostingDate': 'datetime64',
#    'Line.Line': str,
#    'Line.RecordID': str,
    'AccountID': str,  # base="xs:string", <xs:maxLength value="70"/>, <xs:documentation>70 character text.</xs:documentation>
    'StandardAccountID': str, # base="xs:string", <xs:maxLength value="70"/>, <xs:documentation>70 character text.</xs:documentation>
#    'Line.Analysis': 'str',
#    'Line.AnalysisType': 'category',
#    'Line.AnalysisID': 'category',
#    'Line.AnalysisAmount': str,
#    'Line.Amount': float, # OOOOOOPs ... kan være både Tax Amount, og Analysis Amount
    'ValueDate': 'datetime64',
#    'Line.SourceDocumentID': str,
#    'Line.Description': str,
#    'Line.DebitAmount': str,
    'DebitAmount': float,
#    'Line.TaxInformation': str,
#    'TaxType': 'category',
#    'TaxCode': 'category',
#    'TaxPercentage': float,
#    'TaxBase': float,
#    'TaxAmount': float, # Her skulle det kommet en "Amount" rett etterpå ...
#    'Line.ReferenceNumber': str,
#    'Line.SupplierID': str,
    'CreditAmount': float,
#    'Line.CustomerID': str,
    })

    return (lines, orgnr)



#    print(lines)
#    print(lines.iloc[0])
#    print(lines.columns)


#accounts.to_excel("accounts.xlsx")

#lines.to_excel("lines.xlsx")


if __name__ == '__main__':
    path = Path('/home/wslstsk/projects/saft2dataframe/testdata/ExampleFile_SAF-T_Financial_888888888_20180228235959.xml')
    df, orgnr = accounts2df(path)
    print(df)
    print(f'Organisasjonsnummer er: {orgnr}')

    df, orgnr = gle2df(path)
    print(df)
    print(df.columns)
    print(df[['TransactionID', 'Description','DebitAmount', 'TaxAmount', 'CreditAmount']])
    
