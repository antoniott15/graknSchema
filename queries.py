# coding=utf-8
from grakn.client import GraknClient
def print_to_log(title, content):
    print(title)
    print("")
    print(content)
    print("\n")


def getLocationEventQuery(question, transaction):
    print_to_log("Question: ", question)

    query = [
        'match',
        '  $events isa event, has name "thailand";',
        '  (creator: $trainer, creating: $event) isa event;',
        '  $name == "thailand',
        'get $location;'
    ]
    print_to_log("Query:", "\n".join(query))
    query = "".join(query)
    iterator = transaction.query(query)
    answers = iterator.collect_concepts()
    result = [answer.value() for answer in answers]
    print_to_log("Result:", result)
    return result



def execute_query_2(question, transaction):
    print_to_log("Question: ", question)

    query = [
        'match ',
        '  $trainer isa trainers, has dni "72893011";',
        'get $name;'
    ]
    print_to_log("Query:", "\n".join(query))
    query = "".join(query)
    iterator = transaction.query(query)
    answers = iterator.collect_concepts()
    result = [answer.value() for answer in answers]
    print_to_log("Result:", result)
    return result



get_query_examples = [
    {
        "question": "Donde esta situado el evento con nombre thailand",
        "query_function": getLocationEventQuery
    },
    {
        "question": "Como se llama el entrenador con el dni 72893011",
        "query_function": execute_query_2
    }
]


query_examples = get_query_examples

def process_selection(qs_number, keyspace_name):
    ## create a transaction to talk to the phone_calls keyspace
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace=keyspace_name) as session:
            with session.transaction().read() as transaction:
                ## execute the query for the selected question
                question = query_examples[qs_number - 1]["question"]
                query_function = query_examples[qs_number - 1]["query_function"]
                query_function(question, transaction)


if __name__ == "__main__":
    print("")
    print("Que query desea ejecutar?\n")
    for index, qs_func in enumerate(query_examples):
        print(str(index + 1) + ". " + qs_func["question"])
    print("")

    qs_number = -1
    while qs_number < 0 or qs_number > len(query_examples):
        qs_number = int(input("choose a number (0 for to answer all questions): "))
    print("")

    process_selection(qs_number, "thai")