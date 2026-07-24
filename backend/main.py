from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from myenv.myenv.model import Product
from myenv.myenv.database_config import SessionLocal, engine
import myenv.myenv.database_models as database_models
from sqlalchemy.orm import Session

 
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

database_models.Base.metadata.create_all(bind=engine)


      
      


@app.get("/")
def read_root():
    return {"Hello": "World"}

products = [
    Product(id = 1, name = "smart-phone", description = "iphone", price =125000, quantity = 2 ),
    Product(id  = 2, name = "Desktop", description = "LG", price =4500, quantity = 1 ),
    Product(id  = 3, name = "tablet", description = "Lenova",price =12290, quantity = 1 ),
    Product(id  = 4, name = "pendrive",description = "HP", price =1200, quantity = 5 ),

]

def init_db():          

  db = SessionLocal()
  count = db.query(database_models.Product).count()
  if count == 0:

    for product in products:
      db.add(database_models.Product(**product.model_dump()))

      db.commit()
      

init_db()



def get_db():   #to get the data from database
    db = SessionLocal ()

    try:
          yield db
    finally:
          db.close()




@app.get("/products")    #dependencies injections
def product(db: Session = Depends(get_db)):
    #db connection
    
    #query
    db_products = db.query(database_models.Product).all()
    
    return db_products

# Lets call the product by ID

@app.get("/products/{id}")
def  get_product_byid(id : int,db: Session = Depends(get_db )):
     db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
     if db_product:
        return db_product
     return "Product not found"


# lets add the products data by post methode
@app.post("/products")
def add_data_product(product : Product, db: Session = Depends(get_db )):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return product
    

# lets update using Put methode

@app.put("/products/{id}")
def update_product(id : int, product: Product,db: Session = Depends(get_db ) ):
     db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
     if product:
            db_product.name = product.name
            db_product.description = product.description
            db_product.price = product.price
            db_product.quantity = product.quantity
            db.commit()
            return "element added"
        
     return "element not added"

#lets delete the prouct from the list products

@app.delete("/products/{id}")
def delete_product_byid(id : int,db: Session = Depends(get_db )):
     db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
     if db_product:
         db.delete(db_product)
         db.commit()
       
     else:
         return "product not found"
   
   
   

    
