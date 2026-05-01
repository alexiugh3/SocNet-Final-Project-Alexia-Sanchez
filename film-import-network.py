from collections import defaultdict
import tmdbsimple as tmdb # https://github.com/celiao/tmdbsimple/blob/master/tmdbsimple/movies.py
import csv
tmdb.API_KEY = 'b5ae0290f95d8ba53bdb651596b3d7b5'

# for node labels
country_dict = {"FR": "France", "US": "United States", "MX": "Mexico", "IT": "Italy", 
                "NL": "Netherlands", "PL": "Poland", "CZ": "Czech Republic", 
                "CH": "Switzerland", "TH": "Thailand", "TR": "Turkey", "UA": "Ukraine", 
                "LS": "Lesotho", "EG": "Egypt", "NU": "Niue", "CY": "Cyprus", 
                "BD": "Bangladesh", "AT": "Republic of Austria", "IN": "India", "RS": "Serbia", 
                "LT": "Lithuania", "AE": "United Arab Emirates", "EC": "Ecuador", 
                "ZA": "South Africa", "CL": "Chile", "GE": "Georgia", "PY": "Paraguay", 
                "PE": "Peru", "SK": "Slovakia", "KW": "Kuwait", "MY": "Malaysia", 
                "NZ": "New Zealand", "NO": "Norway", "PH": "Philippines", "PT": "Portugal", 
                "RO": "Romania", "RU": "Russia", "SG": "Singapore", "SI": "Slovenia", 
                "TW": "Taiwan", "UY": "Uruguay", "KR": "South Korea", "BR": "Brazil",  
                "HK": "Hong Kong", "DE": "Germany", "GB": "United Kingdom", "CN": "China", 
                "KZ": "Kazakhstan", "VN": "Vietnam", "CA": "Canada", "AR": "Argentina", 
                "ES": "Spain", "FI": "Finland", "HU": "Hungary", "JP": "Japan", 
                "BG": "Bulgaria", "AU": "Australia", "GR": "Greece", "DK": "Denmark", 
                "SE": "Sweden", "BE": "Belgium", "CO": "Colombia", "EE": "Estonia", 
                "HR": "Croatia", "IS": "Iceland", "ID": "Indonesia", "IE": "Ireland", 
                "IL": "Israel", "PR": "Puerto Rico", "BO": "Bolivia", "VE": "Venezuela", 
                "CU": "Cuba", "SV": "El Salvador", "DO": "Dominican Republic", 
                "GT": "Guatemala", "HT": "Haiti", "HN": "Honduras", "PA": "Panama", 
                "ME": "Montenegro", "XK": "Kosovo", "BA": "Bosnia and Herzegovina", 
                "BH": "Bahrain", "OM": "Oman", "QA": "Qatar", "SA": "Saudi Arabia", 
                "LV": "Latvia", "MN": "Mongolia", "BW": "Botswana", "GH": "Ghana", 
                "KE": "Kenya", "NA": "Namibia", "SZ": "Eswatini", "TZ": "Tanzania", 
                "UG": "Uganda", "ZM": "Zambia", "ZW": "Zimbabwe", "NI": "Nicaragua", 
                "AD": "Andorra", "VI": "U.S. Virgin Islands", "MO": "Macao", 
                "LU": "Luxembourg", "JO": "Jordan", "BY": "Belarus", "ML": "Mali", 
                "TN": "Tunisia", "TG": "Togo", "SN": "Senegal", "TF": "French Southern Territories", 
                "AN": "Netherlands Antilles", "RW": "Rwanda", "PK": "Pakistan", 
                "PG": "Papua New Guinea", "NP": "Nepal", "NG": "Nigeria", "NE": "Niger", 
                "MU": "Mauritius", "MZ": "Mozambique", "MG": "Madagascar", "MT": "Malta", 
                "MA": "Morocco", "JM": "Jamaica", "GN": "Guinea", "GA": "Gabon", "DZ": "Algeria", 
                "CM": "Cameroon", "CI": "Côte d'Ivoire", "CG": "Republic of the Congo", 
                "CD": "Democratic Republic of the Congo", "BJ": "Benin", "BF": "Burkina Faso", 
                "UZ": "Uzbekistan", "TT": "Trinidad and Tobago", "TJ": "Tajikistan", 
                "MK": "North Macedonia", "MD": "Moldova", "LK": "Sri Lanka", "KH": "Cambodia", 
                "KG": "Kyrgyzstan", "FJ": "Fiji", "CR": "Costa Rica", "BS": "Bahamas", 
                "AZ": "Azerbaijan", "AO": "Angola", "AM": "Armenia", "AL": "Albania", "LA": "Laos", 
                "GU": "Guam", "MP": "Northern Mariana Islands", "AS": "American Samoa", 
                "MM": "Myanmar", "AG": "Antigua and Barbuda", "AI": "Anguilla", "AW": "Aruba", 
                "BB": "Barbados", "BM": "Bermuda", "BZ": "Belize", "CC": "Cocos (Keeling) Islands", 
                "CK": "Cook Islands", "CX": "Christmas Island", "DM": "Dominica", "FK": "Falkland Islands", 
                "FO": "Faroe Islands", "GD": "Grenada", "GI": "Gibraltar", "GL": "Greenland", 
                "GS": "South Georgia and the South Sandwich Islands", "GY": "Guyana", 
                "IO": "British Indian Ocean Territory", "KN": "Saint Kitts and Nevis", "KY": "Cayman Islands", 
                "LC": "Saint Lucia", "LI": "Liechtenstein", "MH": "Marshall Islands", "MS": "Montserrat", 
                "NF": "Norfolk Island", "PN": "Pitcairn Islands", "SH": "Saint Helena", 
                "SJ": "Svalbard and Jan Mayen", "SM": "San Marino", "SR": "Suriname", 
                "TC": "Turks and Caicos Islands", "TK": "Tokelau", "VA": "Vatican City", 
                "VC": "Saint Vincent and the Grenadines", "VG": "British Virgin Islands", 
                "GP": "Guadeloupe", "MC": "Monaco", "RE": "Réunion", "IQ": "Iraq", "LB": "Lebanon", 
                "NC": "New Caledonia", "CV": "Cape Verde", "FM": "Micronesia", "GM": "Gambia", 
                "GW": "Guinea-Bissau", "TM": "Turkmenistan", "AF": "Afghanistan", "AQ": "Antarctica", 
                "BI": "Burundi", "BN": "Brunei", "BT": "Bhutan", "CF": "Central African Republic", 
                "DJ": "Djibouti", "EH": "Western Sahara", "ER": "Eritrea", "ET": "Ethiopia", 
                "GF": "French Guiana", "GQ": "Equatorial Guinea", "HM": "Heard Island and McDonald Islands", 
                "IR": "Iran", "KI": "Kiribati", "KM": "Comoros", "LR": "Liberia", "LY": "Libya", 
                "MQ": "Martinique", "MR": "Mauritania", "MV": "Maldives", "MW": "Malawi", "NR": "Nauru", 
                "PF": "French Polynesia", "PM": "Saint Pierre and Miquelon", "PS": "Palestine", 
                "PW": "Palau", "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan", 
                "SL": "Sierra Leone", "SO": "Somalia", "SS": "South Sudan", "ST": "São Tomé and Príncipe", 
                "TD": "Chad", "TL": "Timor-Leste", "TO": "Tonga", "TV": "Tuvalu", 
                "UM": "United States Minor Outlying Islands", "VU": "Vanuatu", "WF": "Wallis and Futuna", 
                "WS": "Samoa", "YE": "Yemen", "YT": "Mayotte"}


def createEdges():
    edges = defaultdict(int) # film imports
    movies = []

    discover = tmdb.Discover()
    for page in range(1, 51):  # ~658 movies
        res = discover.movie(**{
            "primary_release_date.gte": "2023-01-01",
            "primary_release_date.lte": "2023-12-31",
            "sort_by": "popularity.desc",
            "vote_count.gte": 100,
            "page": page
        })
        movies.extend(res["results"])

    for m in movies:
        movie = tmdb.Movies(m["id"])
        info = movie.info()
        
        if info["status"] != "Released":
            continue

        origins = [c["iso_3166_1"] for c in info["production_countries"]]

        releases = movie.releases()

        showings = []

        for r in releases['countries']:
            if r["release_date"][0:4] == "2023":
                showings.append(r['iso_3166_1'])

        for c1 in origins:
            for c2 in showings:
                if c1 != c2:
                    edges[(c1, c2)] += 1
    
    print("Created Edges")

    return edges


def exportGraph(edges):
    # trim nodes and edges
    # MIN_WEIGHT = 3

    # filtered_edges = {
    #     (s, t): w
    #     for (s, t), w in edges.items()
    #     if w >= MIN_WEIGHT
    # }

    nodes = sorted({
        country
        for edge in edges
        for country in edge
    })

    # create nodes
    with open("nodes.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # header
        writer.writerow(["Id", "Label"])
        
        for v in nodes:
            label = country_dict.get(v, v)  # fallback to code if missing
            writer.writerow([v, label])

    # create edges
    with open("edges.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # header
        writer.writerow(["Source", "Target", "Weight"])
        
        for (source, target), weight in edges.items():
            if weight > 0:
                writer.writerow([source, target, weight])
    
    print("Exported Graph")

    return False


def main():
    edges = createEdges()
    # exportGraph(edges)


if __name__ == "__main__":
    main()
