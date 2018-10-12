import csv
import subprocess
import httplib2
import ssl

with open('Makerspaces.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    ERROR_file = open("ERROR.txt", "w")
    ACTIVE_file = open("ACTIVE.txt", "w")
    for row in csv_reader:
        Status = ""
        #if line_count == 0:
         #   line_count += 1
        #else:
        print(f'\t{row[0]} {row[2]} {row[3]}')
        DomainName = row[3]
        if DomainName == "":
            ERROR_file.write(DomainName + "\n")
            ERROR_file.write("No URL found in data file")
        else:
            try:
                resp, content = httplib2.Http().request(DomainName)
                if (resp.status == 200):
                    ACTIVE_file.write(str(row))
                    ACTIVE_file.write("\n")
                else:
                    ERROR_file.write(DomainName + "\n")
                    Status = str(resp.status)
                    ERROR_file.write(Status)
            except httplib2.RelativeURIError:
                ERROR_file.write(DomainName + "\n")
                ERROR_file.write(" Not an Absolute URL \n")
                Status = str(resp.status)
                ERROR_file.write(Status + "\n")
            except httplib2.ServerNotFoundError:
                ERROR_file.write(DomainName + "\n")
                ERROR_file.write(" No Server Found \n")
                Status = str(resp.status)
                ERROR_file.write(Status + "\n")
            except ssl.SSLError:
                ERROR_file.write(DomainName + "\n")
                ERROR_file.write(" SSL Error \n")
                Status = str(resp.status)
                ERROR_file.write(Status + "\n")
            except httplib2.RedirectLimit:
                ERROR_file.write(DomainName + "\n")
                ERROR_file.write(" Redirect Limit Reached \n")
                Status = str(resp.status)
                ERROR_file.write(Status + "\n")
    print(f'Processed all websites in file')
    ERROR_file.close()
    ACTIVE_file.close()