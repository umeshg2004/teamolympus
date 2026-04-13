import streamlit as st
import requests
from typing import Optional

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Banking App", layout="wide")


def api_post(path: str, json: dict, token: Optional[str] = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.post(f"{API_BASE_URL}{path}", json=json, headers=headers, timeout=10)


def api_get(path: str, params: Optional[dict] = None, token: Optional[str] = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.get(f"{API_BASE_URL}{path}", params=params, headers=headers, timeout=10)


def api_patch(path: str, json: dict, token: Optional[str] = None):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    return requests.patch(f"{API_BASE_URL}{path}", json=json, headers=headers, timeout=10)


def ensure_state(key: str, default):
    if key not in st.session_state:
        st.session_state[key] = default


def normalize_text(value: str) -> str:
    return value.strip()


def validate_email(value: str) -> bool:
    return "@" in value and "." in value.split("@")[-1]


def safe_rerun() -> None:
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


def parse_int(value: str) -> Optional[int]:
    value = value.strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


ensure_state("customer_token", None)
ensure_state("admin_token", None)
ensure_state("staff_token", None)

st.title("Banking App")

col_left, col_right = st.columns([2, 1])
with col_left:
    pass

st.divider()

st.sidebar.title("Portal")
portal = st.sidebar.radio("Role", ["Customer", "Admin", "Staff"], index=0)

if portal == "Customer":
    token = st.session_state.customer_token
    if token:
        st.sidebar.success("Customer logged in")
        if st.sidebar.button("Logout"):
            st.session_state.customer_token = None
            safe_rerun()
        menu = st.sidebar.radio(
            "Actions",
            ["Add Money", "Withdraw Money", "Transfer Money", "Close Account", "Raise Query"],
        )
    else:
        menu = st.sidebar.radio("Access", ["Register", "Login"])

    if not token and menu == "Register":
        st.subheader("Customer Register")
        c_username = st.text_input("Username", key="c_reg_username")
        c_password = st.text_input("Password", type="password", key="c_reg_password")
        c_name = st.text_input("Full name", key="c_reg_name")
        c_email = st.text_input("Email", key="c_reg_email")
        c_phone = st.text_input("Phone", key="c_reg_phone")
        if st.button("Register Customer"):
            c_username = normalize_text(c_username)
            c_name = normalize_text(c_name)
            c_email = normalize_text(c_email)
            c_phone = normalize_text(c_phone)
            if not c_email or not validate_email(c_email):
                st.error("Enter a valid email address.")
            elif not c_username or not c_password or not c_name:
                st.error("Username, password, and full name are required.")
            else:
                resp = api_post(
                    "/auth/register",
                    {
                        "username": c_username,
                        "password": c_password,
                        "role": "customer",
                        "full_name": c_name,
                        "email": c_email,
                        "phone": c_phone or None,
                    },
                )
                if resp.ok:
                    st.success("Registered")
                else:
                    st.error(resp.text)

    if not token and menu == "Login":
        st.subheader("Customer Login")
        c_luser = st.text_input("Email", key="c_login_username")
        c_lpass = st.text_input("Password", type="password", key="c_login_password")
        if st.button("Login"):
            resp = api_post("/auth/login", {"email": c_luser, "password": c_lpass, "role": "customer"})
            if resp.ok:
                st.session_state.customer_token = resp.json().get("access_token")
                st.success("Logged in")
                safe_rerun()
            else:
                st.error(resp.text)

    rows = []
    if token:
        st.subheader("My Accounts")
        accounts_resp = api_get("/customer/accounts", token=token)
        if accounts_resp.ok:
            rows = accounts_resp.json()
            if rows:
                st.dataframe(rows, use_container_width=True)
            else:
                st.info("No accounts found.")
        else:
            st.error(accounts_resp.text)

    if token and menu == "Add Money":
        st.subheader("Add Money")
        dep_amt = st.number_input("Amount", min_value=0.0, step=10.0, key="dep_amt")
        if st.button("Deposit"):
            if not rows:
                st.error("No account found for your profile.")
            else:
                account_id = rows[0].get("id")
                resp = api_post("/customer/deposit", {"account_id": account_id, "amount": dep_amt}, token)
                if resp.ok:
                    payload = resp.json()
                    st.success(f"Amount added. New balance: {payload.get('balance')}")
                    safe_rerun()
                else:
                    st.error(resp.text)

    if token and menu == "Withdraw Money":
        st.subheader("Withdraw Money")
        w_amt = st.number_input("Amount", min_value=0.0, step=10.0, key="w_amt")
        if st.button("Withdraw"):
            if not rows:
                st.error("No account found for your profile.")
            else:
                account_id = rows[0].get("id")
                resp = api_post("/customer/withdraw", {"account_id": account_id, "amount": w_amt}, token)
                if resp.ok:
                    payload = resp.json()
                    st.success(f"Withdrawal successful. New balance: {payload.get('balance')}")
                    safe_rerun()
                else:
                    st.error(resp.text)

    if token and menu == "Transfer Money":
        st.subheader("Transfer Money")
        to_acc = st.text_input("To account ID", key="to_acc")
        t_amt = st.number_input("Amount", min_value=0.0, step=10.0, key="t_amt")
        if st.button("Transfer"):
            if not rows:
                st.error("No account found for your profile.")
            else:
                from_acc = rows[0].get("id")
                to_id = parse_int(to_acc)
                if not to_id:
                    st.error("Enter a valid target account ID.")
                else:
                    resp = api_post(
                        "/customer/transfer",
                        {"from_account_id": int(from_acc), "to_account_id": to_id, "amount": t_amt},
                        token,
                    )
                    if resp.ok:
                        st.success("Transfer completed.")
                        safe_rerun()
                    else:
                        st.error(resp.text)

    if token and menu == "Close Account":
        st.subheader("Close Account")
        if st.button("Close"):
            if not rows:
                st.error("No account found for your profile.")
            else:
                account_id = rows[0].get("id")
                resp = api_post("/customer/close", {"account_id": account_id}, token)
                if resp.ok:
                    st.success("Account closed.")
                    safe_rerun()
                else:
                    st.error(resp.text)

    if token and menu == "Raise Query":
        st.subheader("Raise Query")
        message = st.text_area("Describe your issue")
        if st.button("Submit Query"):
            resp = api_post("/customer/request", {"message": message}, token)
            if resp.ok:
                st.success("Query submitted.")
            else:
                st.error(resp.text)

if portal == "Admin":
    token = st.session_state.admin_token
    if token:
        st.sidebar.success("Admin logged in")
        if st.sidebar.button("Logout"):
            st.session_state.admin_token = None
            safe_rerun()

        st.sidebar.subheader("Filters")
        status = st.sidebar.selectbox("Status", ["", "active", "closed"], index=0)
        customer_id = st.sidebar.number_input("Customer ID", min_value=0, step=1, value=0)
        balance_min = st.sidebar.number_input("Min balance", min_value=0.0, step=10.0)
        balance_max = st.sidebar.number_input("Max balance", min_value=0.0, step=10.0)
        sort_by = st.sidebar.selectbox("Sort by", ["created_at", "balance", "id"], index=0)
        sort_order = st.sidebar.selectbox("Sort order", ["desc", "asc"], index=0)
        st.subheader("Admin Account Overview")
        params = {
            "status": status or None,
            "customer_id": int(customer_id) if customer_id > 0 else None,
            "balance_min": balance_min if balance_min > 0 else None,
            "balance_max": balance_max if balance_max > 0 else None,
            "sort_by": sort_by,
            "sort_order": sort_order,
        }
        resp = api_get("/admin/accounts", params=params, token=token)
        if resp.ok:
            rows = resp.json()
            if rows:
                st.dataframe(rows, use_container_width=True)
                balances = [row.get("balance", 0) for row in rows]
                if balances:
                    st.caption("Account balances chart")
                    st.bar_chart(balances)
            else:
                st.info("No accounts found for the selected filters.")
        else:
            st.error(resp.text)
    else:
        st.sidebar.subheader("Admin Access")
        admin_menu = st.sidebar.radio("Access", ["Register", "Login"], index=0)

        if admin_menu == "Register":
            st.subheader("Admin Register")
            a_name = st.text_input("Full name", key="a_reg_name")
            a_email = st.text_input("Email", key="a_reg_email")
            a_secret = st.text_input("Secret Code", type="password", key="a_reg_secret")
            if st.button("Register Admin"):
                a_name = normalize_text(a_name)
                a_email = normalize_text(a_email)
                if not a_email or not validate_email(a_email):
                    st.error("Enter a valid email address.")
                elif not a_name:
                    st.error("Full name is required.")
                elif not a_secret:
                    st.error("Secret code is required for admin registration.")
                else:
                    resp = api_post(
                        "/auth/register",
                        {
                            "role": "admin",
                            "full_name": a_name,
                            "email": a_email,
                            "phone": None,
                            "secret_code": a_secret,
                        },
                    )
                    if resp.ok:
                        st.success("Registered")
                    else:
                        st.error(resp.text)

        if admin_menu == "Login":
            st.subheader("Admin Login")
            a_luser = st.text_input("Email", key="a_login_username")
            a_secret = st.text_input("Secret Code", type="password", key="a_login_secret")
            if st.button("Login Admin"):
                resp = api_post("/auth/login", {"email": a_luser, "secret_code": a_secret, "role": "admin"})
                if resp.ok:
                    st.session_state.admin_token = resp.json().get("access_token")
                    st.success("Logged in")
                    safe_rerun()
                else:
                    st.error(resp.text)

if portal == "Staff":
    token = st.session_state.staff_token
    if token:
        st.sidebar.success("Staff logged in")
        if st.sidebar.button("Logout"):
            st.session_state.staff_token = None
            safe_rerun()

        st.subheader("Service Requests")
        resp = api_get("/staff/requests", token=token)
        if resp.ok:
            rows = resp.json()
            if rows:
                st.dataframe(rows, use_container_width=True)
                st.subheader("Mark Request As Solved")
                req_id = st.number_input("Request ID", min_value=1, step=1, key="staff_req_id")
                if st.button("Mark Solved"):
                    upd = api_patch(f"/staff/requests/{int(req_id)}", {"status": "solved"}, token)
                    if upd.ok:
                        payload = upd.json()
                        st.success(f"Request {payload.get('request_id')} marked as {payload.get('new_status')}.")
                        safe_rerun()
                    else:
                        st.error(upd.text)
            else:
                st.info("No requests available.")
        else:
            st.error(resp.text)
    else:
        st.sidebar.subheader("Staff Access")
        staff_menu = st.sidebar.radio("Access", ["Register", "Login"], index=0)

        if staff_menu == "Register":
            st.subheader("Staff Register")
            s_name = st.text_input("Full name", key="s_reg_name")
            s_email = st.text_input("Email", key="s_reg_email")
            s_password = st.text_input("Password", type="password", key="s_reg_password")
            if st.button("Register Staff"):
                s_name = normalize_text(s_name)
                s_email = normalize_text(s_email)
                if not s_email or not validate_email(s_email):
                    st.error("Enter a valid email address.")
                elif not s_name or not s_password:
                    st.error("Full name and password are required.")
                else:
                    resp = api_post(
                        "/auth/register",
                        {
                            "username": s_email,
                            "password": s_password,
                            "role": "staff",
                            "full_name": s_name,
                            "email": s_email,
                            "phone": None,
                        },
                    )
                    if resp.ok:
                        st.success("Registered")
                    else:
                        st.error(resp.text)

        if staff_menu == "Login":
            st.subheader("Staff Login")
            s_email = st.text_input("Email", key="s_login_email")
            s_password = st.text_input("Password", type="password", key="s_login_password")
            if st.button("Login Staff"):
                resp = api_post("/auth/login", {"email": s_email, "password": s_password, "role": "staff"})
                if resp.ok:
                    st.session_state.staff_token = resp.json().get("access_token")
                    st.success("Logged in")
                    safe_rerun()
                else:
                    st.error(resp.text)
