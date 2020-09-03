from flask import render_template, redirect, url_for, flash, request, Blueprint,session
from flask_login import  current_user,  login_required
from the_app._bank.forms import Customer_form, Search_for_customer, Go_to_account, Create_account, Cash_in_out, Money_transfer, Search_form
from the_app._bank.models import add_new_customer, get_customer,update_customer,get_all_customers, get_customers_by_name, get_accounts, get_account, get_last_transactions, add_new_account, make_transaction, get_transaction_details


bankBP = Blueprint('bankBP',__name__,template_folder='templates')

@bankBP.route('/bank')
@login_required
def bank_home():
    return render_template('bank_home.html')


@bankBP.route('/bank_customer', methods=['GET','POST'])
@login_required
def bank_customer():

    form = Customer_form()
    if form.validate_on_submit():
        cust_num=add_new_customer(first_name=form.first_name.data,
                                    last_name=form.last_name.data,
                                    email=form.email.data,
                                    address=form.address.data,
                                    city=form.city.data,
                                    birth_date=form.birth_date.data
                                    )
        flash(f"Dane klienta {cust_num} - {form.first_name.data} {form.last_name.data} zostały zapisane")
        form.customer_number.data=cust_num
        #return render_template('customer.html', form=form)
        return redirect ((url_for('bankBP.update_bank_customer', cust_num=cust_num)))

    return render_template('customer.html', form=form, editable=False)

@bankBP.route('/bank_customer/<cust_num>', methods=['GET','POST'])
@login_required
def update_bank_customer(cust_num):
    form = Customer_form()

    if request.method == 'GET':
        customer = get_customer(cust_num)
        form.first_name.data=customer[2]
        form.last_name.data=customer[3]
        form.email.data=customer[4]
        form.address.data=customer[5]
        form.city.data=customer[6]
        form.birth_date.data=customer[9]
        form.customer_number.data = customer[1]
        form.enrollment_date.data = customer[8]
    
    if form.validate_on_submit():
        update_customer(cust_num=cust_num,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        address=form.address.data,
                        city=form.city.data,
                        birth_date=form.birth_date.data)
        flash(f"Dane klienta {cust_num} - {form.first_name.data} {form.last_name.data} zostały zaktualizowane")

        return redirect ((url_for('bankBP.update_bank_customer', cust_num=cust_num)))
        #return render_template('bank_home.html')

    return render_template('customer.html', form=form, editable=True)


@bankBP.route('/bank_customers', methods=['GET','POST'])
@login_required
def bank_all_customers():
    customers = get_all_customers()
    form = Search_for_customer()

    if form.validate_on_submit():
        name=form.name.data
        return redirect ((url_for('bankBP.bank_search_customers', name=name)))
    return render_template ('bank_customers.html',customers=customers, form=form)

@bankBP.route('/bank_customers/<name>', methods=['GET', 'POST'])
@login_required
def bank_search_customers(name):
    customers = get_customers_by_name(name)
    form = Search_for_customer()
    if request.method == 'GET':
        form.name.data=name

    if form.validate_on_submit():
        name=form.name.data
        return redirect ((url_for('bankBP.bank_search_customers', name=name)))


    return render_template ('bank_customers.html',customers=customers, form=form)



@bankBP.route('/bank_customer_page/<cust_num>', methods=['GET', 'POST'])
@login_required
def bank_customer_page(cust_num):

    form=Go_to_account()
    customer = get_customer(cust_num)
    accounts = get_accounts(cust_num)
    sum_ = 0
    for account in accounts:
        sum_+=account[2]
    if form.validate_on_submit():
        account_num = form.account.data
        return redirect((url_for('bankBP.bank_account_page', account_num=account_num)))

    return render_template('bank_customer_page.html', customer=customer, accounts=accounts, sum_=sum_, form=form)



@bankBP.route('/bank_account_page/<account_num>')
@login_required
def bank_account_page(account_num):
    account = get_account(account_num)
    customer = get_customer(account[4])
    transactions = get_last_transactions(account_num)

    return render_template('bank_account_page.html', customer=customer, account=account, transactions=transactions)

@bankBP.route('/bank_create_account/<customer_num>', methods=['GET', 'POST'])
@login_required
def bank_create_new_account(customer_num):
    form=Create_account()
    if form.validate_on_submit():
        account_name=form.account_name.data
        add_new_account(customer_num, account_name)
        return redirect(url_for('bankBP.bank_customer_page', cust_num=customer_num))

    return render_template('bank_create_new_account.html', customer_num=customer_num, form=form)

@bankBP.route('/bank_cash_in/<account_num>' , methods=['GET', 'POST'])
@login_required
def bank_cash_in(account_num):
    form=Cash_in_out()
    title= 'Wpłata do kasy na rachunek '
    if form.validate_on_submit():
        quote = form.quote.data
        message = make_transaction(account_num,1001,quote,'cash','WPŁATA DO KASY')
        flash(message[0],message[1])
        return redirect(url_for('bankBP.bank_account_page', account_num=account_num))
    return render_template('bank_cash_in_out.html', form=form, account_num=account_num, title=title)


@bankBP.route('/bank_cash_out/<account_num>' , methods=['GET', 'POST'])
@login_required
def bank_cash_out(account_num):
    form=Cash_in_out()
    title= 'Wypłata z kasy z rachunku '
    if form.validate_on_submit():
        quote = form.quote.data
        message = make_transaction(1001,account_num,quote,'cash','WYPŁATA Z KASY')
        flash(message[0],message[1])
        return redirect(url_for('bankBP.bank_account_page', account_num=account_num))
    return render_template('bank_cash_in_out.html', form=form, account_num=account_num,title=title)

@bankBP.route('/bank_wire_transfer/<account_num>', methods=['GET', 'POST'])
@login_required
def bank_wire_transfer(account_num):
    form = Money_transfer()
    if form.validate_on_submit():
        account_in = form.target_account_number.data
        account_out = account_num
        quote = form.quote.data
        transaction_type = 'transfer'
        transaction_title = form.transfer_title.data

        message = make_transaction(account_in,account_out, quote, transaction_type,transaction_title)
        flash(message[0],message[1])
        return redirect(url_for('bankBP.bank_account_page', account_num = account_num))
    return render_template('bank_wire_transfer.html', form=form, account_num=account_num)

@bankBP.route('/bank_transaction_details/<transaction_num>', methods=['GET', 'POST'])
@login_required
def bank_transaction_details(transaction_num):
    transactions = get_transaction_details(transaction_num)
    return render_template('bank_transaction_details.html', transactions=transactions)

@bankBP.route('/bank_search', methods=['GET', 'POST'])
@login_required
def bank_search():
    form= Search_form()
    if form.validate_on_submit():
        search_item = form.search_result.data

        if  len(search_item)==4:
            if search_item[0]=='5':
                return redirect((url_for('bankBP.bank_customer_page', cust_num=search_item)))
            elif search_item[0]=='9':
                return redirect((url_for('bankBP.bank_account_page', account_num=search_item)))
            elif search_item[0]=='7':
                return redirect((url_for('bankBP.bank_transaction_details', transaction_num=search_item)))
            else:
                flash('Nieprawidłowe kryteruim wyszukiwania! Numery muszą zaczyanć się odpowiednio dla poszukiwanego elementu 5-, 9-, 7-.')
                return render_template('bank_search.html', form=form)
        else:
                flash('Nieprawidłowe kryteruim wyszukiwania! Wyszukiwarka dziala dla numerów 4 cyfrowych.')
                return render_template('bank_search.html', form=form)
                
    return render_template('bank_search.html', form=form)



