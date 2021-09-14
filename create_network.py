import networkx as nx

class create_tube():

    def __init__(self): 
        self.G = nx.Graph()

    def lines(self):

        self.G.add_edges_from([("Sloane Square",'Victoria'),('Westminster','Embankment'),("Victoria","St James's Park"),("St James's Park","Westminster"), ('Embankment', 'Temple'), ('Sloane Square','South Kensington'), ('South Kensington','Gloucester Road'), ('Gloucester Road', 'High Street Kensington'),('High Street Kensington', 'Notting Hill Gate'), ('Notting Hill Gate','Bayswater'), ('Bayswater','Edgware Road'), ('South Kensington', "Earl's Court"),("Earl's Court", 'West Brompton'), ('West Brompton','Fulham Broadway'), ('Fulham Broadway', 'Parsons Green'), ('Parsons Green','Putney Bridge'), ('Putney Bridge', 'East Putney'), ('East Putney', 'Southfields'), ('Southfields', 'Wimbledon Park'), ('Wimbledon Park', 'Wimbledon'), ("Earl's Court", 'West Kensington'), ('West Kensington', 'Hammersmith'),('Hammersmith', 'Ravenscourt Park'),('Ravenscourt Park','Stamford Brook'), ('Stamford Brook', 'Turnham Green'), ('Turnham Green', 'Chiswick Park'),('Chiswick Park','Acton Town'), ('Acton Town', 'Ealing Common'), ('Ealing Common', 'Ealing Broadway'),('Turnham Green', 'Gunnersbury'), ('Gunnersbury', 'Kew Gardens'), ('Kew Gardens', 'Richmond'), ('Temple', 'Blackfriars'), ('Blackfriars', 'Mansion House'), ('Mansion House', 'Canon Street'),('Canon Street', 'Monument'), ('Monument','Tower Hill'),('Tower Hill', 'Aldgate East'), ('Aldgate East','Whitechapel')], color = 'Green') #District Line

        self.G.add_edges_from([('Victoria', 'Green Park'),('Victoria', 'Pimlico'),('Pimlico', 'Vauxhall'),('Vauxhall', 'Stockwell'),('Stockwell','Brixton'),('Green Park', 'Oxford Circus'), ('Oxford Circus', 'Warren Street'), ('Warren Street','Euston'),('Euston', "King's Cross St Pancras"),("King's Cross St Pancras",'Highbury and Islington'),('Highbury and Islington', 'Finsbury Park'), ('Finsbury Park', 'Seven Sisters'), ('Seven Sisters', 'Tottenham Hale'),('Tottenham Hale', 'Blackhorse Road'),('Blackhorse Road', 'Walthamstow Central')], color = 'dodgerblue') 

        self.G.add_edges_from([('Green Park','Picadilly Circus'), ('Green Park', 'Hyde Park Corner'), ('Hyde Park Corner', 'Knightsbridge'),('Knightsbridge','South Kensington'), ('South Kensington','Gloucester Road'), ('Picadilly Circus', 'Leicester Square'), ('Leicester Square', 'Covent Garden'), ('Covent Garden', 'Holborn'),('Holborn', 'Russell Square'), ('Russell Square', "King's Cross St Pancras")], color = 'darkblue')

        self.G.add_edges_from([('Picadilly Circus', 'Charing Cross'),('Charing Cross', 'Embankment'), ('Embankment', 'Waterloo'), ('Waterloo', 'Lambeth North'), ('Lambeth North', 'Elephant and Castle'), ('Picadilly Circus', 'Oxford Circus'), ('Oxford Circus', 'Baker Street'), ('Baker Street', 'Marylebone'), ('Marylebone', 'Edgware Road'), ('Edgware Road', 'Paddington')], color = 'brown')

        self.G.add_edges_from([('Notting Hill Gate', 'Queensway'), ('Queensway', 'Lancaster Gate'),('Lancaster Gate', 'Marble Arch'),('Marble Arch','Bond Street'), ('Bond Street','Oxford Circus'), ('Oxford Circus', 'Holborn'), ('Holborn', 'Chancery Lane'),('Chancery Lane', "St Paul's"),("St Paul's", 'Bank'), ('Bank','Moorgate'),('Moorgate', 'Liverpool Street')], color = 'red')

        self.G.add_edges_from([('Baker Street', 'Bond Street'),('Bond Street', 'Green Park'),('Green Park', 'Westminster'),('Westminster', 'Waterloo'),('Waterloo', 'Southwark'),('Southwark','London Bridge')], color = 'grey')
        self.G = self.G.to_directed() 

        return self.G