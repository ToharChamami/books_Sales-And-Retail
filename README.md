Tohar Levi-Chamami 215108549
Eden Naomi-Hashay 210042453

# books_Sales-And-Retail

1.Introduction and System Description.

2.System analysis TOP DOWN


### ***1.***

This system was designed to manage the sales and retail department of a national bookstore chain.
The system provides a comprehensive solution for managing daily branch activities such as inventory management and more.



#### ***System boundaries and key processes -***



**Catalog and inventory management:** tracking book inventory at each branch, including technical data and genres.

**Customer and Customer Club Management:** Customer registration and club membership dates for future promotions.

**Sales system:** Real-time transaction documentation, including contanting the employee making the purchase and the purchasing customer.

**Workforce Management:** Tracking employees across different branches and their roles.




### ***2.***

At this stage, we have characterized the system interfaces using Google AI Studio.
The goal is to understand the business needs and data flow before building the database.
Below is the characterization of the four screens.


![img.png](img.png)
![img_1.png](img_1.png)
![img_2.png](img_2.png)
![img_3.png](img_3.png)
![img_4.png](img_4.png)
![img_5.png](img_5.png)



---

## Phase 3: ERD & Database Schema Design (DSD) & Normalization

### 1. Conceptual Design - Entity Relationship Diagram (ERD)

Based on the system screens and user requirements characterized in Phase 2, I have designed the following ERD (Entity Relationship Diagram). This diagram models the 10 core entities and the relationships required to support the application logic
![img_7.png](img_7.png)

### Data Dictionary

#### 1. Table: Genre
**Purpose:** Manages book categories to ensure data consistency and avoid duplication.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **G_ID** | INT | PRIMARY KEY | Unique identifier for each genre. |
| **Genre_Name** | VARCHAR(255) | NOT NULL | The name of the category (e.g., Fiction, Science, History). |

#### 2. Table: Publisher
**Purpose:** Stores information about the publishing houses the bookstore works with.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **P_ID** | INT | PRIMARY KEY | Unique identifier for the publisher. |
| **Publisher_Name** | VARCHAR(255) | NOT NULL | The official name of the publishing house. |

#### 3. Table: Branch
**Purpose:** Manages physical bookstore locations and logistics.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **Branch_ID** | INT | PRIMARY KEY | Unique branch identification number. |
| **Branch_Name** | VARCHAR(255) | NOT NULL | Name of the specific branch. |
| **City** | VARCHAR(255) | - | The city where the branch is located. |
| **Address** | VARCHAR(255) | - | Full physical address of the branch. |
| **Manager_ID** | INT | - | ID of the employee managing this branch. |

#### 4. Table: Customer
**Purpose:** Maintains records for bookstore customers and loyalty club members.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **C_ID** | INT | PRIMARY KEY | Unique customer identification number. |
| **Full_Name** | VARCHAR(255) | NOT NULL | Full name of the customer. |
| **Phone** | VARCHAR(50) | - | Contact phone number. |
| **Email** | VARCHAR(255) | - | Customer's email address. |
| **Join_Date** | DATE | - | The date the customer joined the system (Significant Date 1). |
| **Loyalty_Info** | JSON | - | Flexible data regarding points and rewards in JSON format. |

#### 5. Table: Employee
**Purpose:** Manages human resources and staff assignments across branches.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **E_ID** | INT | PRIMARY KEY | Unique employee identification number. |
| **First_Name** | VARCHAR(255) | NOT NULL | Employee's first name. |
| **Last_Name** | VARCHAR(255) | NOT NULL | Employee's last name. |
| **Position** | VARCHAR(255) | - | The job title/role of the employee. |
| **Hire_Date** | DATE | - | The date the employee started working. |
| **Salary** | DECIMAL(10,2) | - | Monthly salary with two decimal precision. |
| **Branch_ID** | INT | FOREIGN KEY | Links the employee to their assigned branch. |

#### 6. Table: Book
**Purpose:** The central catalog of all book titles available in the retail network.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **Book_ID** | INT | PRIMARY KEY | Unique identifier for the book (e.g., ISBN). |
| **Title** | VARCHAR(255) | NOT NULL | The title of the book. |
| **Author** | VARCHAR(255) | - | The name of the book's author. |
| **Price** | DECIMAL(10,2) | - | The catalog price of the book. |
| **Publication_Date**| DATE | - | Official release date (Significant Date 2). |
| **B_Data** | JSON | - | Additional metadata and attributes in JSON format. |
| **G_ID** | INT | FOREIGN KEY | Links the book to its respective Genre. |
| **P_ID** | INT | FOREIGN KEY | Links the book to its respective Publisher. |

#### 7. Table: Sale
**Purpose:** Records the header information for every sales transaction.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **S_ID** | INT | PRIMARY KEY | Unique transaction/invoice number. |
| **Sale_Date** | DATE | - | The date the transaction occurred. |
| **Total_Amount** | DECIMAL(10,2) | - | Final total amount paid for the transaction. |
| **Payment_Method** | VARCHAR(50) | - | Method of payment (e.g., Cash, Credit Card). |
| **Receipt_Data** | JSON | - | Digital copy of the receipt stored in JSON. |
| **C_ID** | INT | FOREIGN KEY | The customer who made the purchase. |
| **E_ID** | INT | FOREIGN KEY | The employee who processed the sale. |

#### 8. Table: Inventory
**Purpose:** Manages the M:N relationship between branches and books.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **Branch_ID** | INT | PK, FK | Link to the specific branch. |
| **Book_ID** | INT | PK, FK | Link to the specific book. |
| **Quantity** | INT | DEFAULT 0 | Number of copies currently in stock at this branch. |

#### 9. Table: Sale_Item
**Purpose:** Detail table recording each specific book included in a sale.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| **S_ID** | INT | PK, FK | Link to the main Sale record. |
| **Book_ID** | INT | PK, FK | Link to the specific book purchased. |
| **Quantity** | INT | NOT NULL | The number of units purchased in this transaction. |

### 2. Database Normalization Analysis
In this phase, I converted the ERD into a relational schema. Each table was analyzed to ensure it meets the requirements of **BCNF (Boyce-Codd Normal Form)** or **3NF**, minimizing redundancy and ensuring data integrity.

| Table Name | Functional Dependencies (FDs) | Normalization Level | Logic / Justification |
| :--- | :--- | :--- | :--- |
| **Genre** | `{G_ID} -> {Genre_Name}` | **BCNF** | The ID is the only determinant and it is a Candidate Key. |
| **Publisher** | `{P_ID} -> {Publisher_Name}` | **BCNF** | Simple key with no transitive dependencies. |
| **Branch** | `{Branch_ID} -> {Branch_Name, City, Address, Manager_ID}` | **BCNF** | All non-key attributes are fully dependent on the Branch_ID. |
| **Customer** | `{C_ID} -> {Full_Name, Phone, Email, Join_Date, Loyalty_Info}` | **BCNF** | Every determinant is a Superkey. |
| **Employee** | `{E_ID} -> {First_Name, Last_Name, Position, Hire_Date, Salary, Branch_ID}` | **BCNF** | Standard 1:N relationship; no partial dependencies. |
| **Book** | `{Book_ID} -> {Title, Author, Price, Publication_Date, B_Data, G_ID, P_ID}` | **BCNF** | Full dependency on the Book_ID. |
| **Sale** | `{S_ID} -> {Sale_Date, Total_Amount, Payment_Method, Receipt_Data, C_ID, E_ID}` | **BCNF** | All sale data depends strictly on the unique Transaction ID. |
| **Inventory** | `{Branch_ID, Book_ID} -> {Quantity}` | **BCNF** | Composite Primary Key. Quantity depends on the specific pair. |
| **Sale_Item** | `{S_ID, Book_ID} -> {Quantity}` | **BCNF** | Composite Primary Key. Quantity depends on the specific Sale/Book pair. |

> **Note on Normalization:** All tables are in **BCNF** because for every non-trivial functional dependency $X \to Y$, $X$ is a superkey. There are no transitive or partial dependencies.

---

### 3. SQL Data Definition Language (DDL)
The following SQL commands implement the design in the PostgreSQL database:
The full SQL script can be found in init-db/01-schema.sql
```sql
-- 1. Simple Entities
CREATE TABLE Genre (
    G_ID INT PRIMARY KEY,
    Genre_Name VARCHAR(255) NOT NULL
);

CREATE TABLE Publisher (
    P_ID INT PRIMARY KEY,
    Publisher_Name VARCHAR(255) NOT NULL
);

CREATE TABLE Branch (
    Branch_ID INT PRIMARY KEY,
    Branch_Name VARCHAR(255) NOT NULL,
    City VARCHAR(255),
    Address VARCHAR(255),
    Manager_ID INT
);

CREATE TABLE Customer (
    C_ID INT PRIMARY KEY,
    Full_Name VARCHAR(255) NOT NULL,
    Phone VARCHAR(50),
    Email VARCHAR(255),
    Join_Date DATE,
    Loyalty_Info JSON
);

-- 2. Entities with Foreign Keys (1:N Relationships)
CREATE TABLE Employee (
    E_ID INT PRIMARY KEY,
    First_Name VARCHAR(255) NOT NULL,
    Last_Name VARCHAR(255) NOT NULL,
    Position VARCHAR(255),
    Hire_Date DATE,
    Salary DECIMAL(10,2),
    Branch_ID INT,
    FOREIGN KEY (Branch_ID) REFERENCES Branch(Branch_ID)
);

CREATE TABLE Book (
    Book_ID INT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Author VARCHAR(255),
    Price DECIMAL(10,2),
    Publication_Date DATE,
    B_Data JSON,
    G_ID INT,
    P_ID INT,
    FOREIGN KEY (G_ID) REFERENCES Genre(G_ID),
    FOREIGN KEY (P_ID) REFERENCES Publisher(P_ID)
);

CREATE TABLE Sale (
    S_ID INT PRIMARY KEY,
    Sale_Date DATE,
    Total_Amount DECIMAL(10,2),
    Payment_Method VARCHAR(50),
    Receipt_Data JSON,
    C_ID INT,
    E_ID INT,
    FOREIGN KEY (C_ID) REFERENCES Customer(C_ID),
    FOREIGN KEY (E_ID) REFERENCES Employee(E_ID)
);

-- 3. Junction Tables (M:N Relationships)
CREATE TABLE Inventory (
    Branch_ID INT,
    Book_ID INT,
    Quantity INT DEFAULT 0,
    PRIMARY KEY (Branch_ID, Book_ID),
    FOREIGN KEY (Branch_ID) REFERENCES Branch(Branch_ID),
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID)
);

CREATE TABLE Sale_Item (
    S_ID INT,
    Book_ID INT,
    Quantity INT NOT NULL,
    PRIMARY KEY (S_ID, Book_ID),
    FOREIGN KEY (S_ID) REFERENCES Sale(S_ID),
    FOREIGN KEY (Book_ID) REFERENCES Book(Book_ID)
);
```
![img_6.png](img_6.png)
---

## Phase 4: Data Population, Backup & Restore

### 1. Data Population Methods
The database was populated using three distinct methods to reach over 20,000 records:
* **Python (Faker Library):** Generated mass data for Sales and Customers.
The script generates relational data while maintaining referential integrity between tables.
![img_12.png](img_8.png)
![img_9.png](img_9.png)

* **CSV Import:** Imported structured data for Branches, Publishers, and Inventory.

![img_11.png](img_11.png)
![img_12.png](img_12.png)
![img_14.png](img_14.png)
* **Mockaroo:** Generated the Employee table in SQL format.


### 2. Backup & Restore Procedures
To ensure data durability, I implemented two backup strategies:
1. **Full Backup (Custom Format):** A complete binary backup of the database.
2. **Schema-Only Backup:** A backup of the table structures.

#### **Restore Verification**
The backup was tested by restoring it into a new database named `books_restore_test`. 
* **Verification Query:** `SELECT COUNT(*) FROM Sale;`
* **Result:** The system successfully recovered all records.

#### **System Proof (Screenshots):**
![Backup Process1](screenshot-backup1.png)
![Backup Process2](screenshot-backup2.png)
![Restore Success](screenshot-restore1.png)
![Data Verification](screenshot-restore2.png)
