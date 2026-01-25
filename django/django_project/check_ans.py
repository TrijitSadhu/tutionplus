from bank.models import currentaffairs_mcq

for mcq_id in [36, 37, 38, 39, 40]:
    mcq = currentaffairs_mcq.objects.get(id=mcq_id)
    print(f'MCQ {mcq_id}:')
    print(f'  Question: {mcq.question[:60]}...')
    print(f'  Answer (ans field): {mcq.ans}')
    print(f'  Correct Option: Option {mcq.ans}')
    print(f'  Option 1: {mcq.option_1[:40]}...')
    print(f'  Option 2: {mcq.option_2[:40]}...')
    print(f'  Option 3: {mcq.option_3[:40]}...')
    print(f'  Option 4: {mcq.option_4[:40]}...')
    print()
