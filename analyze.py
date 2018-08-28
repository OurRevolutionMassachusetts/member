from member.Member import Member
import csv


def main():
    file = './all_members.csv'

    # load the csv file of all members
    data = csv.DictReader(open(file, 'U'))
    members = [Member(csv=row) for row in data]

    report_unaffiliated(members=members)

    #mysteries = [m for m in members if m.affiliate is None and m.unaffiliated is None and m.city is None and m.zip_code is None]
    #print(len(mysteries))

    #print(*([m.zip_code for m in members if m.city is None and m.zip_code is not None]), sep="\n")




def report_unaffiliated(members):
    unaffiliated = {}

    total = 0
    for m in members:
        if m.unaffiliated is not False:
            city = str(m.city)
            if not city in unaffiliated:
                unaffiliated[city] = []
            unaffiliated[city].append(m)
            total += 1

    print(total)
    cities = list(unaffiliated.keys())
    cities.sort()
    print(*(c for c in cities), sep="\n")


main()