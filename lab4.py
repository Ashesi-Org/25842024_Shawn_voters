# from https://pythonbasics.org/flask-rest-api/

import json
from flask import Flask, request, jsonify

app = Flask(__name__)


# Registering a student as a voter
@app.route('/register-voter', methods=['POST'])
def register_voter():
    record = json.loads(request.data)
    with open('voters.json', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        for r in records:
            if r['ID'] == record['ID']:
                return jsonify({"error": "Voter already exists"})
        records.append(record)
    with open('voters.txt', 'w') as f:
        f.write(json.dumps(records))
    return jsonify(record)


# De-registering a Student as a Voter
@app.route('/voter/<id>', methods=['DELETE'])
def deregister_voter(id):
    with open('voters.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['ID'] == int(id):
                records.remove(r)
                with open('voters.txt', 'w') as f:
                    f.write(json.dumps(records))
                return jsonify(r)

        return jsonify({"error": "student not found"}), 404


# Updating a voter
@app.route('/update_voter/<id>', methods=['PUT'])
def update_voter(id):
    if not request.data:
        return jsonify({"error": "no data has been entered"})

    with open('voters.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r["ID"] == int(id):
                r["name"] = request.json["name"]
                r["major"] = request.json["major"]
                r["class"] = request.json["class"]
                with open('voters.txt', 'w') as f:
                    f.write(json.dumps(records))
                return jsonify(r)
        return jsonify({"error": "student not found"}), 404


# Retrieving a registered voter
@app.route('/retrieve-voter', methods=['GET'])
def retrieve_voter():
    student = json.loads(request.data)
    print(student)

    with open('voters.json', 'r') as f:
        data = f.read()
        if data:
            records = json.loads(data)
            for r in records:
                if r['ID'] == student['ID']:
                    return jsonify({
                        'id': r['ID'],
                        'name': r['name'],
                        'major': r['major'],
                        'class': r['class']
                    })

                else:
                    return jsonify({"error": "student not found"}), 404


# Creating an Election
@app.route('/create_election', methods=['POST'])
def create_election():
    record = json.loads(request.data)
    with open('election.txt', 'r') as f:
        data = f.read()
    if not data:
        records = [record]
    else:
        records = json.loads(data)
        for r in records:
            if r['electionID'] == record['electionID']:
                return jsonify({"error": "Election already exists"})

        records.append(record)
    with open('election.txt', 'w') as f:
        f.write(json.dumps(records))
    return jsonify(record)


# Retrieving an Election
@app.route('/retrieve_election/<id>', methods=['GET'])
def retrieve_election(id):

    with open('election.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['electionID'] == id:
                return jsonify(r)

        return jsonify({"error": "Election not found"}), 404


# Deleting an Election


@app.route('/delete_election/<id>', methods=['DELETE'])
def delete_election(id):
    with open('election.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r['electionID'] == id:
                records.remove(r)
                with open('election.txt', 'w') as f:
                    f.write(json.dumps(records))
                return jsonify(r)

        return jsonify({"error": "election not found"}), 404


# Voting in an Election
@app.route('/election/<electionid>/<candidateid>', methods=['PATCH'])
def vote_election(electionid, candidateid):
    with open('election.txt', 'r') as f:
        data = f.read()
        records = json.loads(data)
        for r in records:
            if r["electionID"] == electionid:
                for candidate in r["candidates"]:
                    if candidate["candidateID"] == candidateid:
                        candidate["votesCast"] += 1
                        with open('election.txt', 'w') as f:
                            f.write(json.dumps(records))
                        return jsonify(r)
                return jsonify({"error": "candidate not found"}), 404
        return jsonify({"error": "election not found"}), 404


app.run(debug=True, port=5000)
