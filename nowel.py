#!/usr/bin/env python3

import os
import random
import sys
import yaml


def parse_config():
    print("Parsing config...")

    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')

    with open(config_path, 'r') as stream:
        try:
            return yaml.load(stream)
        except Exception as e:
            print(f"Error while parsing config: {e}", file=sys.stderr)

def choose_random_pairing(gifter, receivers, participants, first_gifter):
    if len(participants) == 1:
        first_gifter = None

    possible_choices = [
        p for p in receivers
        if p not in participants[gifter]['exclusions']
        if p != gifter
        if p != first_gifter
    ]

    return random.choice(possible_choices)

def choose_pairings(participants, receivers):
    remaining_participants = participants.copy()
    pairings = []

    first_gifter = random.choice([p for p in remaining_participants.keys()])
    last_receiver = first_gifter

    while remaining_participants:
        gifter = last_receiver
        receiver = choose_random_pairing(gifter, receivers, remaining_participants, first_gifter)

        pairings.append({
            "gifter_name": gifter,
            "gifter_email": participants[gifter]['mail'],
            "receiver_name": receiver,
            "receiver_email": participants[receiver]['mail']
        })

        del remaining_participants[gifter]
        receivers.remove(receiver)

        last_receiver = receiver

    return pairings

def generate_pairings(list):
    print("Generating pairings...")

    participants = {}
    receivers = []

    for p in list['participants']:
        name, mail = p.split('/')

        participants[name] = {'mail': mail, 'exclusions': []}
        receivers.append(name)

    for p in participants:
        participants[p]['receivers'] = [r for r in receivers if r != p]

    for e in list['exclusions']:
        p1, p2 = e.split('/')

        participants[p1]['exclusions'].append(p2)
        participants[p2]['exclusions'].append(p1)

    while True:
        try:
            return choose_pairings(participants.copy(), receivers.copy())
        except Exception as e:
            print("Trying pairings again...")

def send_emails(pairings, mail):
    for p in pairings:
        gifter = p['gifter_name']
        receiver = p['receiver_name']
        
        print(f"\t{gifter} -> {receiver}")

    print("Send emails ? [y/N] ")

    choice = input().lower()

    if choice != 'y':
        return

    print("Sending emails...")

if __name__ == "__main__":
    config = parse_config()
    pairings = generate_pairings(config['list'])
    send_emails(pairings, config['mail'])