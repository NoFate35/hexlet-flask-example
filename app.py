from flask import Flask, render_template, request

from data import generate_users

users = generate_users(100)

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)
@app.route('/users')
def get_users():
    
    template_users = users
    query = request.args.get('term', None)
    if query:
        template_users = filter(lambda user: user['first_name'].lower().startswith(query.lower()), users)
    return render_template('users/index.html',
                               users=list(template_users),
                               search=query)
    '''
    query = request.args.get('term', None)
    print('term', query, 'request.args', request.args)
    if query is None:
        print('truuuuuu')
        return render_template('users/index.html',
                               template_users=users)
    len_query = len(query)
    filter_users = []
    for user in users:
        if user['first_name'][:len_query].lower() == query.lower():
            filter_users.append(user)        
        
    print('query', query, 'filter_users', list(filter_users), '\n')
    return render_template('users/index.html',
                           template_users=filter_users,
                           search=query)
     '''                    
# END

