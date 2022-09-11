from neo4j import GraphDatabase, basic_auth
import socket


class Movie_queries(object):
    def __init__(self, password):
        self.driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", password), encrypted=False)
        self.session = self.driver.session()
        self.transaction = self.session.begin_transaction()

    def q0(self):
        result = self.transaction.run("""
            MATCH (n:Actor) RETURN n.name, n.id ORDER BY n.birthday ASC LIMIT 3
        """)
        return [(r[0], r[1]) for r in result]

    def q1(self):
        result = self.transaction.run("""
        MATCH (n:Actor)-[:ACTS_IN]->(movie:Movie)
        Return n.name, Count(movie.title) AS Count
        ORDER BY Count DESC, n.name ASC
        LIMIT 20;
        
            
        """)
        return [(r[0], r[1]) for r in result]

    def q2(self):
        result = self.transaction.run("""
        
        MATCH (movie:Movie)<-[:RATED]-(person:Person)
        WITH movie, collect(movie) as rated
        MATCH (actor:Actor)-[:ACTS_IN]->(m:Movie)
        WHERE m in rated
        Return m.title,count(*) as count
        ORDER BY count DESC
        Limit 1
        """)
        return [(r[0], r[1]) for r in result]

    def q3(self):
        result = self.transaction.run("""
        Match (d:Director)-[:DIRECTED]->(m:Movie)
        where exists (m.genre)
        with d, count(Distinct m.genre) as count
        where count>1
        return d.name,count
        order by count DESC,d.name ASC
        """)
        return [(r[0], r[1]) for r in result]

    def q4(self):
        result = self.transaction.run("""
         MATCH (Kev:Actor{name:"Kevin Bacon"})-[:ACTS_IN]->(m:Movie) <-[:ACTS_IN]-(co:Actor)
            MATCH (co)-[:ACTS_IN]->(m2:Movie)<-[:ACTS_IN]-(co2:Actor)
            WHERE Kev <> co2 AND NOT (Kev)-[:ACTS_IN]->(:Movie)<-[:ACTS_IN]-(co2)
            RETURN DISTINCT co2.name
            ORDER by co2.name
            
        """)
        return [(r[0]) for r in result]

if __name__ == "__main__":
    sol = Movie_queries("neo4jpass")
    print("---------- Q0 ----------")
    print(sol.q0())
    print("---------- Q1 ----------")
    print(sol.q1())
    print("---------- Q2 ----------")
    print(sol.q2())
    print("---------- Q3 ----------")
    print(sol.q3())
    print("---------- Q4 ----------")
    print(sol.q4())
    sol.transaction.close()
    sol.session.close()
    sol.driver.close()

