import psycopg2
import psycopg2.extras
import json
import os

# TODO hostname
conn = psycopg2.connect(
    os.getenv("POSTGRES_URL"),
    cursor_factory=psycopg2.extras.RealDictCursor,
)


def setup_schema():
    schema = open("schema.sql", "r").read()

    with conn.cursor() as cur:
        cur.execute(schema)
        conn.commit()


def insert_user(email, password_hash, type):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash, type) VALUES (%s, %s, %s) returning id",
        (email, password_hash, type),
    )
    user_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return user_id


def get_user(email):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user


def get_user_by_id(id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    return user


def change_password(user_id, password_hash):
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET password_hash = %s WHERE id = %s",
        (password_hash, user_id),
    )
    conn.commit()
    cur.close()


def get_safe_user(id):
    cur = conn.cursor()
    cur.execute(
        """
        select
            to_jsonb(u.*) - 'password_hash' user,
            to_jsonb(p.*) || jsonb_build_object('strengths', coalesce(jsonb_agg(s.name) FILTER (WHERE ps.profile_id IS NOT NULL), '[]')) :: jsonb || json_build_object('title', t.name) :: jsonb || jsonb_build_object('interests', coalesce(jsonb_agg(i.name) FILTER (WHERE pi.profile_id IS NOT NULL), '[]')) :: jsonb profile
        from
            users u
            left join profiles p on p.user_id = u.id
            left join profile_strengths ps on ps.profile_id = p.id
            left join profile_interests pi on pi.profile_id = p.id
            left join strengths s on s.id = ps.strength_id
            left join interests i on i.id = pi.interest_id
            left join titles t on t.id = p.title_id
        where
            u.id = %s
        group by
            u.id,
            p.id,
            ps.profile_id,
            pi.profile_id,
            t.name
    """,
        (id,),
    )
    user = cur.fetchone()
    cur.close()
    return user


def get_all_safe_mentors():
    cur = conn.cursor()
    cur.execute(
        """
        select
            to_jsonb(u.*) - 'password_hash' user,
            to_jsonb(p.*) || jsonb_build_object('strengths', coalesce(jsonb_agg(s.name) FILTER (WHERE ps.profile_id IS NOT NULL), '[]')) :: jsonb || json_build_object('title', t.name) :: jsonb || jsonb_build_object('interests', coalesce(jsonb_agg(i.name) FILTER (WHERE pi.profile_id IS NOT NULL), '[]')) :: jsonb profile
        from
            users u
            left join profiles p on p.user_id = u.id
            left join profile_strengths ps on ps.profile_id = p.id
            left join profile_interests pi on pi.profile_id = p.id
            left join strengths s on s.id = ps.strength_id
            left join interests i on i.id = pi.interest_id
            left join titles t on t.id = p.title_id
        where
            u.type = 'mentor'
        group by
            u.id,
            p.id,
            ps.profile_id,
            pi.profile_id,
            t.name
    """
    )
    mentors = cur.fetchall()
    cur.close()
    return mentors


def get_all_safe_mentees():
    cur = conn.cursor()
    cur.execute(
        """
        select
            to_jsonb(u.*) - 'password_hash' user,
            to_jsonb(p.*) || jsonb_build_object('strengths', coalesce(jsonb_agg(s.name) FILTER (WHERE ps.profile_id IS NOT NULL), '[]')) :: jsonb || json_build_object('title', t.name) :: jsonb || jsonb_build_object('interests', coalesce(jsonb_agg(i.name) FILTER (WHERE pi.profile_id IS NOT NULL), '[]')) :: jsonb profile
        from
            users u
            left join profiles p on p.user_id = u.id
            left join profile_strengths ps on ps.profile_id = p.id
            left join profile_interests pi on pi.profile_id = p.id
            left join strengths s on s.id = ps.strength_id
            left join interests i on i.id = pi.interest_id
            left join titles t on t.id = p.title_id
        where
            u.type = 'mentee'
        group by
            u.id,
            p.id,
            ps.profile_id,
            pi.profile_id,
            t.name
    """
    )
    mentees = cur.fetchall()
    cur.close()
    return mentees


def insert_mentee(user_id, mentor_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mentee (user_id, mentor_id) VALUES (%s, %s) returning id",
        (user_id, mentor_id),
    )
    mentee_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return mentee_id


def insert_mentor(user_id, mentee_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mentor (user_id, mentee_id) VALUES (%s, %s) reuturning id",
        (user_id, mentee_id),
    )
    mentor_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    return mentor_id


def add_mentee_mentor(user_id, mentor_id):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO mentee_mentors (mentee_user_id, mentor_user_id) VALUES (%s, %s)",
        (user_id, mentor_id),
    )
    conn.commit()
    cur.close()


def insert_profile(
    user_id,
    role_id,
    title_id,
    city_id,
    country_id,
    gender,
    theatre_id,
    bio,
    csap_track,
    same_theatre,
    same_gender,
    same_role,
    first_priority,
    second_priority,
    strengths,
    interests,
):
    cur = conn.cursor()
    cur.execute(
        """
            INSERT INTO profiles (
              user_id,
              role_id,
              title_id,
              city_id,
              country_id,
              gender,
              theatre_id,
              bio,
              csap_track,
              same_theatre,
              same_gender,
              same_role,
              first_priority,
              second_priority
            ) VALUES (
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s,
              %s
            ) returning id
            """,
        (
            user_id,
            role_id,
            title_id,
            city_id,
            country_id,
            gender,
            theatre_id,
            bio,
            csap_track,
            same_theatre,
            same_gender,
            same_role,
            first_priority,
            second_priority,
        ),
    )
    profile_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    insert_profile_strengths(profile_id, strengths)
    insert_profile_interests(profile_id, interests)
    return profile_id


def insert_profile_strengths(profile_id, strengths):
    cur = conn.cursor()
    for strength in strengths:
        cur.execute(
            "INSERT INTO profile_strengths (profile_id, strength_id) VALUES (%s, %s)",
            (profile_id, strength),
        )
    conn.commit()
    cur.close()


def insert_profile_interests(profile_id, interests):
    cur = conn.cursor()
    for interest in interests:
        cur.execute(
            "INSERT INTO profile_interests (profile_id, interest_id) VALUES (%s, %s)",
            (profile_id, interest),
        )
    conn.commit()
    cur.close()


def get_user_mentor(user_id):
    cur = conn.cursor()
    cur.execute(
        """
        select
            to_jsonb(u2.*) - 'password_hash' user,
            to_jsonb(p.*) || jsonb_build_object(
                'strengths',
                coalesce(
                    jsonb_agg(s.name) FILTER (
                        WHERE
                            ps.profile_id IS NOT NULL
                    ),
                    '[]'
                )
            ) :: jsonb || json_build_object('title', t.name) :: jsonb || jsonb_build_object(
                'interests',
                coalesce(
                    jsonb_agg(i.name) FILTER (
                        WHERE
                            pi.profile_id IS NOT NULL
                    ),
                    '[]'
                )
            ) :: jsonb profile,
            mm.room_id
        from
            users u
            inner join mentee_mentors mm on mm.mentee_user_id = u.id
            inner join users u2 on u2.id = mm.mentor_user_id
            inner join profiles p on p.user_id = u2.id
            left join profile_strengths ps on ps.profile_id = p.id
            left join profile_interests pi on pi.profile_id = p.id
            left join strengths s on s.id = ps.strength_id
            left join interests i on i.id = pi.interest_id
            left join titles t on t.id = p.title_id
        where
            u.id = %s
        group by
            u2.id,
            p.id,
            ps.profile_id,
            pi.profile_id,
            t.name,
            mm.room_id
    """,
        (user_id,),
    )
    mentor = cur.fetchone()
    cur.close()
    return mentor


def get_user_mentees(user_id):
    cur = conn.cursor()
    cur.execute(
        """
        select
            to_jsonb(u2.*) - 'password_hash' user,
            to_jsonb(p.*) || jsonb_build_object(
                'strengths',
                coalesce(
                    jsonb_agg(s.name) FILTER (
                        WHERE
                            ps.profile_id IS NOT NULL
                    ),
                    '[]'
                )
            ) :: jsonb || json_build_object('title', t.name) :: jsonb || jsonb_build_object(
                'interests',
                coalesce(
                    jsonb_agg(i.name) FILTER (
                        WHERE
                            pi.profile_id IS NOT NULL
                    ),
                    '[]'
                )
            ) :: jsonb profile,
            mm.room_id
        from
            users u
            inner join mentee_mentors mm on mm.mentor_user_id = u.id
            inner join users u2 on u2.id = mm.mentee_user_id
            inner join profiles p on p.user_id = u2.id
            left join profile_strengths ps on ps.profile_id = p.id
            left join profile_interests pi on pi.profile_id = p.id
            left join strengths s on s.id = ps.strength_id
            left join interests i on i.id = pi.interest_id
            left join titles t on t.id = p.title_id
        where
            u.id = %s
        group by
            u2.id,
            p.id,
            ps.profile_id,
            pi.profile_id,
            t.name,
            mm.room_id
    """,
        (user_id,),
    )
    mentees = cur.fetchall()
    cur.close()
    return mentees


# TODO resolve id's such as title, gender city, country, theatre


def get_all_theatres():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(theatres) theatres FROM theatres")
    theatres = cur.fetchone()
    cur.close()
    return theatres["theatres"]


def get_all_roles():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(roles) roles FROM roles")
    roles = cur.fetchone()
    cur.close()
    return roles["roles"]


def get_all_titles():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(titles) titles FROM titles")
    titles = cur.fetchone()
    cur.close()
    return titles["titles"]


def get_all_cities():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(cities) cities FROM cities")
    cities = cur.fetchone()
    cur.close()
    return cities["cities"]


def get_all_strengths():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(strengths) strengths FROM strengths")
    strengths = cur.fetchone()
    cur.close()
    return strengths["strengths"]


def get_all_interests():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(interests) interests FROM interests")
    interests = cur.fetchone()
    cur.close()
    return interests["interests"]


def get_all_countries():
    cur = conn.cursor()
    cur.execute("SELECT json_agg(countries)  countries FROM countries")
    countries = cur.fetchone()
    cur.close()
    return countries["countries"]


def get_mentor_mentee_link(mentee_id, mentor_id):
    cur = conn.cursor()
    cur.execute(
        "SELECT * from mentee_mentors where mentee_user_id = %s and mentor_user_id = %s",
        (mentee_id, mentor_id),
    )
    mentee_mentors = cur.fetchone()
    cur.close()
    return mentee_mentors


def delete_mentor_mentee_link(mentee_id, mentor_id):
    cur = conn.cursor()
    cur.execute(
        "DELETE from mentee_mentors where mentee_user_id = %s and mentor_user_id = %s",
        (mentee_id, mentor_id),
    )
    conn.commit()
    cur.close()


def add_room(room_id, mentee_id, mentor_id):
    cur = conn.cursor()
    cur.execute(
        "UPDATE mentee_mentors SET room_id = %s WHERE mentee_user_id = %s AND mentor_user_id = %s",
        (room_id, mentee_id, mentor_id),
    )
    conn.commit()
    cur.close()


def delete_room(mentee_id, mentor_id):
    cur = conn.cursor()
    cur.execute(
        "UPDATE mentee_mentors SET room_id = NULL WHERE mentee_user_id = %s AND mentor_user_id = %s",
        (mentee_id, mentor_id),
    )
    conn.commit()
    cur.close()
