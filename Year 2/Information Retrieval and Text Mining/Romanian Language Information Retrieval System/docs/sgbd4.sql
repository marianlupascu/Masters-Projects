--ex4.1
DECLARE
  sir_1 CHAR(10) := 'PL/SQL';
  sir_2 VARCHAR2(10) := 'PL/SQL';  
BEGIN
  IF sir_1 = sir_2 THEN
      DBMS_OUTPUT.PUT_LINE (sir_1 || ' = ' || sir_2);
    ELSE
     DBMS_OUTPUT.PUT_LINE (sir_1 || ' =! ' || sir_2 );
    END IF;
  END;
/

--ex4.2
create table test (d date);
delete from test;

insert into test values (TO_DATE('15-OCT-2012','DD-MON-YYYY'));
insert into test values (TO_DATE('15-OCT-2012 00:00:00','DD-MON-YYYY HH24:MI:SS'));
insert into test values (TO_DATE('15.10.2012  15:22:07','DD.MM.YYYY HH24:MI:SS'));
insert into test values (sysdate);

select dump(d) from test;

--ex4.3
SELECT DUMP(TO_DATE('15-OCT-2012 00:00:00','DD-MON-YYYY HH24:MI:SS'))
FROM DUAL;

SELECT DUMP(SYSDATE)
FROM DUAL;


--ex4.4
DECLARE
  SUBTYPE subtip_data IS DATE NOT NULL;
  SUBTYPE subtip_email IS CHAR(15);
  SUBTYPE subtip_desctirere IS VARCHAR2(1500);
  SUBTYPE subtip_rang IS PLS_INTEGER RANGE -5..5;
  SUBTYPE subtip_test IS BOOLEAN;
  v_data subtip_data := SYSDATE;
  v_email subtip_email(10);
  v_descriere subtip_desctirere;
  v_rang subtip_rang := 2;
  v_test BOOLEAN;
BEGIN
   NULL;
END;
/

--ex4.5
DECLARE
  TYPE rec IS RECORD 
        (id   categorii.id_categorie%TYPE, 
         den  categorii.denumire%TYPE, 
         niv  categorii.nivel%TYPE);
  v_categ rec;
  v_categ2 rec;
BEGIN
  v_categ.den := 'Categorie noua';
  v_categ.niv :=1;
  SELECT MAX(id_categorie)+1 INTO v_categ.id 
  FROM   categorii;
  
  -- eroare
  --INSERT INTO categorii(id_categorie, denumire, nivel) VALUES v_categ;
  INSERT INTO categorii(id_categorie, denumire, nivel) 
  VALUES (v_categ.id, v_categ.den, v_categ.niv);
  SELECT id_categorie, denumire, nivel INTO v_categ2
  FROM   categorii
  WHERE  id_categorie= v_categ.id;
  
  DBMS_OUTPUT.PUT_LINE ('Ati inserat: '|| v_categ2.id || ' ' || v_categ2.den || '  '|| v_categ2.niv);
END;
/

--ex4.6
DECLARE
  v_categ categorii%ROWTYPE;
  v_categ2 categorii%ROWTYPE;
  v_categ_modific v_categ%ROWTYPE;
  v_categ_null categorii%ROWTYPE;
BEGIN
  v_categ.denumire := 'Categorie noua';
  v_categ.nivel :=1;
  SELECT MAX(id_categorie)+1 INTO v_categ.id_categorie 
  FROM   categorii;
  
  INSERT INTO categorii VALUES v_categ;
  
  SELECT * INTO v_categ2
  FROM   categorii
  WHERE  id_categorie= v_categ.id_categorie;
  
  DBMS_OUTPUT.PUT_LINE ('Ati inserat: '|| v_categ2.id_categorie ||
       ' ' || v_categ2.denumire || '  '|| v_categ2.nivel || ' ' || NVL(v_categ2.id_parinte,0));
       
 v_categ_modific := v_categ;
 v_categ_modific.id_categorie := v_categ.id_categorie + 1;
 
 UPDATE categorii
 SET ROW = v_categ_modific
 WHERE  id_categorie= v_categ.id_categorie;
 
 SELECT * INTO v_categ2
 FROM   categorii
 WHERE  id_categorie= v_categ_modific.id_categorie;
 
 DBMS_OUTPUT.PUT_LINE ('Ati modificat in: '|| v_categ_modific.id_categorie ||
       ' ' || v_categ_modific.denumire || '  '|| v_categ_modific.nivel || ' ' || NVL(v_categ_modific.id_parinte,0));
 
 v_categ2 := v_categ_null;
 
 DELETE FROM categorii 
 WHERE  id_categorie= v_categ_modific.id_categorie
 RETURNING id_categorie, denumire, nivel, id_parinte INTO v_categ2;
 
 DBMS_OUTPUT.PUT_LINE ('Ati sters linia: '|| v_categ2.id_categorie ||
       ' ' || v_categ2.denumire || '  '|| v_categ2.nivel || ' ' || NVL(v_categ2.id_parinte,0));

END;
/

--ex4.7
DECLARE
  TYPE tab_ind IS TABLE OF NUMBER INDEX BY PLS_INTEGER;
  t    tab_ind;
BEGIN
  -- atribuire valori
  FOR i IN 1..10 LOOP
    t(i):=i;
  END LOOP;
  -- parcurgere
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- numar elemente
  FOR i IN 1..10 LOOP
    IF i mod 2 = 1 THEN t(i):=null; 
    END IF;
  END LOOP;
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');

  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(nvl(t(i), 0) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  -- stergere elemente
  t.DELETE(t.first);
  t.DELETE(5,7);
  t.DELETE(t.last);
  DBMS_OUTPUT.PUT_LINE('Primul element are indicele ' || 
      t.first || ' si valoarea ' || nvl(t(t.first),0));
  DBMS_OUTPUT.PUT_LINE('Ultimul element are indicele ' || 
      t.last || ' si valoarea ' || nvl(t(t.last),0));
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT || ' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
     IF t.EXISTS(i) THEN 
        DBMS_OUTPUT.PUT(nvl(t(i), 0)|| ' '); 
     END IF;
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  t.DELETE;
  DBMS_OUTPUT.PUT_LINE('Tabloul are ' || t.COUNT 
     ||' elemente.');
END;

/

--ex4.8
DECLARE
  TYPE tab_ind IS TABLE OF produse%ROWTYPE
       INDEX BY PLS_INTEGER;
  t    tab_ind;
BEGIN
  -- atribuire valori
SELECT * BULK COLLECT INTO t
FROM   produse
WHERE  ROWNUM<=10;

  --parcurgere
  DBMS_OUTPUT.PUT_LINE('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT_LINE(t(i).id_produs || ' '||t(i).denumire); 
  END LOOP;
END;
/

--ex4.9
DECLARE
  TYPE tab_ind IS TABLE OF tip_plata.descriere%TYPE
       INDEX BY PLS_INTEGER;
  t    tab_ind;
BEGIN
  -- atribuire valori
DELETE FROM tip_plata
WHERE  id_tip_plata NOT IN (SELECT id_tip_plata FROM facturi)
RETURNING descriere BULK COLLECT INTO t;

  --parcurgere
  DBMS_OUTPUT.PUT_LINE('Tabloul are ' || t.COUNT ||
      ' elemente:');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT_LINE(t(i));
  END LOOP;
ROLLBACK;
END;
/

--ex4.10
DECLARE
  TYPE rec IS RECORD (id tip_plata.id_tip_plata%TYPE,
                      den tip_plata.descriere%TYPE);
  TYPE tab_ind IS TABLE OF rec
       INDEX BY PLS_INTEGER;
  t    tab_ind;
BEGIN
  -- atribuire valori
   DELETE FROM tip_plata
   WHERE  id_tip_plata NOT IN (SELECT id_tip_plata FROM facturi)
   RETURNING id_tip_plata, descriere BULK COLLECT INTO t;

  --parcurgere
  DBMS_OUTPUT.PUT_LINE('Tabloul are ' || t.COUNT ||' elemente:');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT_LINE(t(i).id ||' '|| t(i).den);
  END LOOP;
ROLLBACK;
END;
/

--ex4.11
DECLARE
   TYPE tab_ind IS TABLE OF NUMBER INDEX BY VARCHAR2(1);
   t tab_ind;
   i varchar2(1);

BEGIN
   -- initializare
   t('a') := ASCII('a');
   t('A') := ASCII('A');
   t('b') := ASCII('b');
   t('B') := ASCII('B');
   t('x') := ASCII('x');
   t('X') := ASCII('X');
  
   -- parcurgere
   i := t.FIRST;
   WHILE  i IS NOT NULL  LOOP
     DBMS_OUTPUT.PUT_LINE('t('||i ||')='||t(i));
     i := t.NEXT(i);   
   END LOOP;
END;
/


--ex4.12_a
DECLARE
  TYPE tab_imb IS TABLE OF NUMBER;
  t    tab_imb := tab_imb();
BEGIN
  -- atribuire valori
  FOR i IN 1..10 LOOP
    t.EXTEND;
    t(i):=i;
  END LOOP;
  --parcurgere
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  -- numar elemente
  FOR i IN 1..10 LOOP
    IF i mod 2 = 1 THEN t(i):=null; 
    END IF;
  END LOOP;
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');

  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(nvl(t(i), 0) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  -- stergere elemente
  t.DELETE(t.first);
  t.DELETE(5,7);
  t.DELETE(t.last);
  DBMS_OUTPUT.PUT_LINE('Primul element are indicele ' || 
      t.first || ' si valoarea ' || nvl(t(t.first),0));
  DBMS_OUTPUT.PUT_LINE('Ultimul element are indicele ' || 
      t.last || ' si valoarea ' || nvl(t(t.last),0));
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT || ' elemente: ');
 
  FOR i IN t.FIRST..t.LAST LOOP
     IF t.EXISTS(i) THEN 
        DBMS_OUTPUT.PUT(nvl(t(i), 0)|| ' '); 
     END IF;
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  t.DELETE;
  DBMS_OUTPUT.PUT_LINE('Tabloul are ' || t.COUNT 
     ||' elemente.');
END;
/

--ex12_b
DECLARE
  TYPE tab_imb IS TABLE OF NUMBER;
  t    tab_imb := tab_imb(1,2,3,4,5);
  t_null tab_imb;
BEGIN
  -- atribuire valori
  t.EXTEND(5);
  FOR i IN 6..10 LOOP
    t(i):=i;
  END LOOP;
  --parcurgere
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  t := t_null;
  IF t IS NULL THEN
    DBMS_OUTPUT.PUT_LINE('Colectie atomic null');
  END IF;
END;
/

--ex13
                             
CREATE TYPE t_imb_categ IS TABLE OF VARCHAR2(40);
/

CREATE TABLE raion_grupe_imb
( id_categorie NUMBER(4) PRIMARY KEY,
  denumire     VARCHAR2(40),
  grupe        t_imb_categ)
NESTED TABLE grupe STORE AS tab_imb_grupe;

INSERT INTO raion_grupe_imb
VALUES (1, 'r1', t_imb_categ('r11','r12'));

INSERT INTO raion_grupe_imb
VALUES (2, 'r2', t_imb_categ('r21'));

INSERT INTO raion_grupe_imb(id_categorie, denumire)
VALUES (3,'r3');

UPDATE raion_grupe_imb
SET    grupe = t_imb_categ('r31','r32')
WHERE  id_categorie =3;

SELECT * FROM raion_grupe_imb;

SELECT id_categorie, denumire, b.* 
FROM   raion_grupe_imb  a, TABLE(a.grupe) b;

SELECT grupe 
FROM   raion_grupe_imb
WHERE  id_categorie = 1;

SELECT *
FROM   TABLE(SELECT grupe FROM raion_grupe_imb WHERE id_categorie=1);



--ex4.14
DECLARE
  -- tipul a fost definit la ex4.13
  v_grupe      t_imb_categ := t_imb_categ();
  v_id_categ   raion_grupe_imb.id_categorie%TYPE;
  v_den        raion_grupe_imb.denumire%TYPE;
BEGIN
  SELECT * INTO v_id_categ, v_den, v_grupe
  FROM   raion_grupe_imb
  WHERE  id_categorie = 1;
  
  DBMS_OUTPUT.PUT_LINE(v_id_categ || ' ' || v_den);
  DBMS_OUTPUT.PUT_LINE('---------------------------');
  FOR i IN 1..v_grupe.LAST LOOP
     DBMS_OUTPUT.PUT_LINE(v_grupe(i));
  END LOOP;
END;
/

--ex4.15
DECLARE
  TYPE tab_vec IS VARRAY(10) OF NUMBER;
  t    tab_vec := tab_vec();
BEGIN
  -- atribuire valori
  FOR i IN 1..10 LOOP
    t.EXTEND;
    t(i):=i;
  END LOOP;
  --parcurgere
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;

  -- numar elemente
  FOR i IN 1..10 LOOP
    IF i mod 2 = 1 THEN t(i):=null; 
    END IF;
  END LOOP;
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');

  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(nvl(t(i), 0) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- sterg ultimul element
  t.TRIM(1);
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(nvl(t(i), 0) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- sterg ultimule 2 elemente
  t.TRIM(2);
  DBMS_OUTPUT.PUT('Tabloul are ' || t.COUNT ||' elemente: ');
  FOR i IN t.FIRST..t.LAST LOOP
      DBMS_OUTPUT.PUT(nvl(t(i), 0) || ' '); 
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- stergere elemente
  t.DELETE;
  --t.TRIM(t.COUNT);
  DBMS_OUTPUT.PUT_LINE('Tabloul are ' || t.COUNT 
     ||' elemente.');
END;
/

--ex4.16
CREATE TYPE t_vect_categ IS VARRAY(10) OF VARCHAR2(40);
/

CREATE TABLE raion_grupe_vect
( id_categorie NUMBER(4) PRIMARY KEY,
  denumire     VARCHAR2(40),
  grupe        t_vect_categ);

INSERT INTO raion_grupe_vect
VALUES (1, 'r1', t_vect_categ('r11','r12'));

INSERT INTO raion_grupe_vect
VALUES (2, 'r2', t_vect_categ('r21'));

INSERT INTO raion_grupe_vect (id_categorie, denumire)
VALUES (3,'r3');

UPDATE raion_grupe_vect
SET    grupe = t_vect_categ('r31','r32')
WHERE  id_categorie =3;

SELECT * FROM raion_grupe_vect;

SELECT id_categorie, denumire, b.* 
FROM   raion_grupe_vect  a, TABLE(a.grupe) b;

SELECT grupe 
FROM   raion_grupe_vect
WHERE  id_categorie = 1;

SELECT *
FROM   TABLE(SELECT grupe FROM raion_grupe_vect WHERE id_categorie=1);


--ex4.17
DECLARE
  type t_linie is VARRAY(3) OF INTEGER;
  type matrice IS VARRAY(3) OF t_linie;
  v_linie t_linie := t_linie(4,5,6);
  a    matrice := matrice(t_linie(1,2,3), v_linie);
BEGIN
  -- se adauga un element de tip vector matricei a (o linie noua)
  a.EXTEND;
  -- se adauga valori elementului nou
  a(3) := t_linie(7,8);
  -- se extinde elementul nou
  a(3).EXTEND;
  -- se adauga valoare elementului nou
  a(3)(3) := 9;
 
 FOR i IN 1..3 LOOP
    FOR j IN 1..3 LOOP
      DBMS_OUTPUT.PUT(a(i)(j)||' ');
    END LOOP;
    DBMS_OUTPUT.NEW_LINE;
  END LOOP;
END;
/

--ex4.18
DECLARE
   TYPE t_imb IS TABLE OF NUMBER(2);
   
   t t_imb := t_imb();
   t1 t_imb := t_imb(1,2,1,3,3);
   t2 t_imb := t_imb(1,2,4,2);
   t3 t_imb := t_imb(1,2,4);
   t4 t_imb := t_imb(1,2,4);
   t5 t_imb := t_imb(1,2);
  
BEGIN
  -- IS EMPTY
   IF t IS EMPTY THEN
      DBMS_OUTPUT.PUT_LINE('t nu are elemente');
   END IF;
  
  -- CARDINALITY
  DBMS_OUTPUT.PUT('t1 are '|| CARDINALITY(t1) || ' elemente: ');
  FOR i IN 1..t1.LAST LOOP
      DBMS_OUTPUT.PUT(t1(i)||' ');
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  DBMS_OUTPUT.PUT('t2 are '|| CARDINALITY(t2) || ' elemente: ');
  FOR i IN 1..t2.LAST LOOP
      DBMS_OUTPUT.PUT(t2(i)||' ');
  END LOOP;
  DBMS_OUTPUT.NEW_LINE; 
  
  -- SET
  t:= SET(t1);
  DBMS_OUTPUT.PUT('t1 fara duplicate: ');
  FOR i IN 1..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i)||' ');
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
   
  -- MULTISET EXCEPT
  t := t1 MULTISET EXCEPT t2;
  DBMS_OUTPUT.PUT('t1 minus t2: ');
    FOR i IN 1..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i)||' ');
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- MULTISET UNION
  DBMS_OUTPUT.PUT('t1 union distinct t2: ');
  t := t1 MULTISET UNION DISTINCT t2;
    FOR i IN 1..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i)||' ');
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- MULTISET INSERSECT
  t := t1 MULTISET INTERSECT DISTINCT t2;
  DBMS_OUTPUT.PUT('t1 intersect distinct t2 : ');
    FOR i IN 1..t.LAST LOOP
      DBMS_OUTPUT.PUT(t(i)||' ');
  END LOOP;
  DBMS_OUTPUT.NEW_LINE;
  
  -- test egalitate
  IF t2=t3 THEN 
     DBMS_OUTPUT.PUT_LINE('t2 = t3');
  ELSE
     DBMS_OUTPUT.PUT_LINE('t2 <> t3');
  END IF;
  
  IF t3=t4 THEN 
     DBMS_OUTPUT.PUT_LINE('t3 = t4');
  ELSE
     DBMS_OUTPUT.PUT_LINE('t3 <> t4');
  END IF;
  
  -- IN
  IF t4 IN (t1,t2,t3) THEN 
     DBMS_OUTPUT.PUT_LINE('t4 in (t1,t2,t3)');
  ELSE
     DBMS_OUTPUT.PUT_LINE('t4 not in (t1,t2,t3)');
  END IF;
  
  -- IS A SET
  IF t4 IS A SET THEN
      DBMS_OUTPUT.PUT_LINE('t4 este multime');
  ELSE
     DBMS_OUTPUT.PUT_LINE('t4 nu este multime');
  END IF;
  
  -- MEMBER OF
  IF 2 MEMBER OF t4 THEN
     DBMS_OUTPUT.PUT_LINE('2 este in t4');
  ELSE
     DBMS_OUTPUT.PUT_LINE('2 nu este in t4');
  END IF;
  
  -- SUBMULTISET OF
  IF t5 SUBMULTISET OF t4 THEN
     DBMS_OUTPUT.PUT_LINE('t5 este inclus in t4');
  ELSE
     DBMS_OUTPUT.PUT_LINE('t5 nu este inclus in t4');
  END IF;
END;
/


--ex4.19 (continuare ex4.13)

-- selectie elemente colectie
SELECT *
FROM TABLE (SELECT grupe FROM raion_grupe_imb WHERE id_categorie = 1);

--adaugare element in colectie
INSERT INTO TABLE (SELECT grupe FROM raion_grupe_imb WHERE id_categorie = 1)
VALUES ('r13');

-- adaugare elemente obtinute cu subcerere
INSERT INTO TABLE (SELECT grupe FROM raion_grupe_imb WHERE id_categorie = 1) 
SELECT denumire
FROM   categorii 
WHERE  id_parinte = 1;


-- modificare element colectie
UPDATE TABLE (SELECT grupe FROM raion_grupe_imb WHERE id_categorie = 1) a
SET VALUE(a) =  'r1333'
WHERE COLUMN_VALUE = 'r13';

--stergere element colectie
DELETE FROM TABLE (SELECT grupe FROM raion_grupe_imb WHERE id_categorie = 1) a
WHERE COLUMN_VALUE = 'r1333';


--ex4.20
SELECT denumire 
FROM   categorii
WHERE  id_parinte = 1;;

SELECT CAST (COLLECT(denumire) AS t_imb_categ)
FROM   categorii
WHERE  id_parinte = 1;

SELECT CAST(MULTISET(SELECT denumire 
                     FROM   categorii
                     WHERE  id_parinte=1) 
            AS t_imb_categ)
FROM  DUAL;

--ex4.21
DECLARE
   TYPE t_ind IS TABLE OF categorii.id_categorie%TYPE 
         INDEX BY PLS_INTEGER;
   TYPE t_imb IS TABLE OF categorii.denumire%TYPE;
   TYPE t_vec IS VARRAY(10) OF categorii.nivel%TYPE;
   v_ind t_ind;
   v_imb t_imb;
   v_vec t_vec;
   nr number;
BEGIN
   SELECT id_categorie, denumire, nivel
   BULK COLLECT INTO v_ind, v_imb, v_vec
   FROM  categorii
   WHERE id_parinte = 1;
      
   FOR i IN 1..v_ind.LAST LOOP
     DBMS_OUTPUT.PUT(v_ind(i) || ' ' || v_imb(i) || 
                     ' ' ||v_vec(i));
     DBMS_OUTPUT.NEW_LINE;
  END LOOP;
END;
/

--ex22
DECLARE
  TYPE tab_ind IS TABLE OF tip_plata%ROWTYPE
       INDEX BY PLS_INTEGER;
  t    tab_ind;
BEGIN
  -- atribuire valori
   DELETE FROM tip_plata
   WHERE  id_tip_plata NOT IN (SELECT id_tip_plata 
                               FROM facturi)
   RETURNING id_tip_plata, cod, descriere BULK COLLECT INTO t;
  
  -- insert in tabel
  FOR i IN t.FIRST..t.LAST LOOP
      INSERT INTO tip_plata VALUES t(i); 
  END LOOP;   
END;
/

--ex4.23
DECLARE
  TYPE tab_ind IS TABLE OF tip_plata%ROWTYPE
       INDEX BY PLS_INTEGER;
  t    tab_ind;
BEGIN
  -- atribuire valori
   DELETE FROM tip_plata
   WHERE  id_tip_plata NOT IN (SELECT id_tip_plata 
                               FROM facturi)
   RETURNING id_tip_plata, cod, descriere BULK COLLECT INTO t;
  
  -- insert in tabel
  FORALL i IN t.FIRST..t.LAST 
      INSERT INTO tip_plata VALUES t(i);
END;
/

select * from tip_plata;
            
    

--ex4.24
drop table produse_copie;
CREATE TABLE produse_copie AS SELECT * FROM PRODUSE;

DECLARE
   TYPE tip_vec IS VARRAY(3) OF NUMBER(4);
   v tip_vec := tip_vec(800, 900, 1000);
BEGIN
   FORALL i IN 1..3 
      DELETE FROM produse_copie 
      WHERE id_categorie = v(i);
  
  FOR j in 1..v.LAST LOOP
  DBMS_OUTPUT.PUT_LINE( 'Numar linii procesate la pasul ' || 
         j || ': ' || SQL%BULK_ROWCOUNT(j));  
  END LOOP;  
END;
/
ROLLBACK;
      


--ex4.25

INSERT INTO CATEGORII(id_categorie)
VALUES(9999);

INSERT INTO produse (id_produs, denumire, id_categorie)
VALUES(9999, 'D9999', 9999);
COMMIT;

SELECT id_produs, denumire, id_categorie
FROM   produse
WHERE  id_categorie in (800, 900, 9999) 
ORDER BY 3;

DECLARE
   TYPE tip_vec IS VARRAY(3) OF NUMBER(4);
   v tip_vec := tip_vec(800, 900, 9999);
   eroare EXCEPTION;
  PRAGMA EXCEPTION_INIT(eroare, -24381);
   nr_erori NUMBER;
BEGIN
   FORALL i IN 1..3 SAVE EXCEPTIONS
      DELETE FROM produse 
      WHERE id_categorie = v(i);  
  
 EXCEPTION
   WHEN eroare THEN 
   nr_erori := SQL%BULK_EXCEPTIONS.COUNT;
   DBMS_OUTPUT.PUT_LINE('Numar comenzi esuate: ' || nr_erori);
   FOR i IN 1..nr_erori LOOP
      DBMS_OUTPUT.PUT_LINE('Eroare ' || i || ' aparuta in timpul iteratiei ' 
          || SQL%BULK_EXCEPTIONS(i).ERROR_INDEX); 
      DBMS_OUTPUT.PUT_LINE('Mesajul erorii: ' ||
          SQLERRM(-SQL%BULK_EXCEPTIONS(i).ERROR_CODE));
   END LOOP;
END;
/

SELECT id_produs, denumire, id_categorie
FROM   produse
WHERE  id_categorie in (800, 900, 9999) 
ORDER BY 3;











