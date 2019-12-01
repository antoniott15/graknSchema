from grakn.client import GraknClient
import ijson


def build_phone_call_graph(inputs, data_path, keyspace_name):
    with GraknClient(uri="localhost:48555") as client:  
        with client.session(keyspace=keyspace_name) as session:  
            for input in inputs:
                input["file"] = input["file"].replace(data_path, "")  
                input["file"] = data_path + input["file"]  
                print("Loading from [" + input["file"] + ".json] into Grakn ...")
                load_data_into_grakn(input, session)


def load_data_into_grakn(input, session):
    items = parse_data_to_dictionaries(input)

    for item in items:  # 2
        with session.transaction().write() as transaction:  
            graql_insert_query = input["template"](item) 
            print("Executing Graql Query: " + graql_insert_query)
            transaction.query(graql_insert_query)  
            transaction.commit()  

    print("\nInserted " + str(len(items)) +
          " items from [ " + input["file"] + ".json] into Grakn.\n")


def school_template(school):
    graql_insert_query = 'insert $school isa school, has traineDni "' + \
        school["traineDni"] + '", has studentDNI "'+ school["studentDNI"] + \
            '", has studentsInfo "'+school["studentsInfo"]+'", has location "'+\
                school["location"] + '", has ruc "' + school["ruc"] + '", has about "'+\
                    school["about"] + '", has name "' + school["name"] + '", has email "' +\
                        school["email"] + '", has password "' + school["password"] + '";'
    return graql_insert_query

def trainer_template(trainers):
    graql_insert_query = 'insert $trainers isa trainers, has traineDni "' + \
        trainers["traineDni"] + '", has dni "'+ trainers["dni"] + \
            '", has about "'+trainers["about"]+'", has name "'+\
                trainers["name"] + '", has email "' + trainers["email"] + '", has password "'+\
                    trainers["password"] + '", has yearsExperience "' + trainers["yearsExperience"] + '", has championshipWon "' +\
                        trainers["championshipWon"] +'";'
    return graql_insert_query


def personalSession(personalSession):
    graql_insert_query = 'insert $personalSession isa personalSession, has traineDni "' + \
        personalSession["traineDni"] + '", has studentDNI "'+ personalSession["studentDNI"] + \
            '", has studentsInfo "'+personalSession["studentsInfo"]+'", has location "'+\
                personalSession["location"] + '", has schedule "' + personalSession["schedule"] + '", has duration "'+\
                    personalSession["duration"] + '", has cost "' + personalSession["cost"]  +'";'
    return graql_insert_query





def schoolSession_template(schoolSession):
    graql_insert_query = 'insert $schoolSession isa schoolSession, has traineDni "' + \
        schoolSession["traineDni"] + '", has studentDNI "'+ schoolSession["studentDNI"] + \
            '", has studentsInfo "'+schoolSession["studentsInfo"]+'", has location "'+\
                schoolSession["location"] + '", has schedule "' + schoolSession["schedule"] + '", has duration "'+\
                    schoolSession["duration"] + '", has cost "' + schoolSession["cost"]  +'", has maxStudents "' + schoolSession["maxStudents"]+\
                        '", has minStudents "' + schoolSession["minStudents"] + '";'
    return graql_insert_query


def events_template(events):
    graql_insert_query = 'insert $events isa events, has traineDni "' + \
        events["traineDni"] + '", has studentsInfo "'+events["studentsInfo"]+'", has location "'+ \
                events["location"] + '", has schedule "' + events["schedule"] + '", has title "'+ \
                    events["title"] + '", has cost "' + events["cost"]  + '";'
    return graql_insert_query


def students_template(students):
    graql_insert_query = 'insert $students isa students, has email "' + \
        students["email"] + '", has studentDNI "'+ students["studentDNI"] + \
            '", has studentsInfo "'+students["studentsInfo"]+'", has birdhdate "'+\
                students["birdhdate"] + '", has password "' + students["password"] + '", has name "'+\
                    students["name"] + '";'
    return graql_insert_query


def create_template(create):
    graql_insert_query = 'match $creator isa school, has ruc "'+ create["create_id"] +'";'
    graql_insert_query += ' $creating isa personalSession, has traineDni "'+ create["creating_id"] +'",'
    graql_insert_query += ' $creating isa schoolSession, has traineDni "'+ create["creating_id"] +'",'
    graql_insert_query += ' $creating isa events, has traineDni "'+ create["creating_id"] +'";'
    graql_insert_query += 'match $creator isa trainers, has dni "'+ create["create_id"] +'";'
    graql_insert_query += ' $creating isa personalSession, has traineDni "'+ create["creating_id"] +'",'
    graql_insert_query += ' $creating isa schoolSession, has traineDni "'+ create["creating_id"] +'",'
    graql_insert_query += ' $creating isa events, has traineDni "'+ create["creating_id"] +'";'
    return graql_insert_query
    

def parse_data_to_dictionaries(input):
    items = []
    with open(input["file"] + ".json") as data:
        for item in ijson.items(data, "item"):
            items.append(item) 
    return items


Inputs = [
    {
        "file": "school",
        "template": school_template
    },
    {
        "file": "trainer",
        "template": trainer_template
    },
    {
        "file": "personalSession",
        "template": personalSession
    },
    {
        "file": "schoolSession",
        "template": schoolSession_template
    },
    {
        "file": "events",
        "template": events_template
    },
    {
        "file": "students",
        "template": create_template
    },
    {
        "file": "create",
        "template": create_template
    }
]

if __name__ == "__main__":
    build_phone_call_graph(inputs=Inputs, data_path="./data/", keyspace_name = "thai")
