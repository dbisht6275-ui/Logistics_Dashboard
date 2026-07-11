import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


@st.cache_resource
def get_engine():
    """
    Cached engine — built only ONCE per app session, then reused.
    Without this, every Streamlit rerun (every filter change) was
    creating a brand new connection pool from scratch.
    """

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(3),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _build_engine():
        connection_url = URL.create(
            "mssql+pymssql",
            username=st.secrets["DB_USER"],
            password=st.secrets["DB_PASSWORD"],
            host=st.secrets["DB_SERVER"],
            port=int(st.secrets["DB_PORT"]),
            database=st.secrets["DB_NAME"],
        )

        return create_engine(
            connection_url,
            pool_pre_ping=True,
            pool_recycle=1800,
            pool_size=5,
            max_overflow=10,
        )

    return _build_engine()