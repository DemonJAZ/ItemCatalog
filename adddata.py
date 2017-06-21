from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Brands, Base, Items, Users
import autopep8

engine = create_engine('sqlite:///brandProducts.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# items By Nike
brand1 = Brands(name="Nike", user_id = 1)
session.add(brand1)
session.commit()

Item1 = Items(name = "NIKE MERCURIAL SUPERFLY V CR7 FG", image = "http://images.nike.com/is/image/DotCom/PDP_HERO_M/852511_001_A_PREM/mercurial-superfly-v-cr7-firm-ground-soccer-cleat.jpg",
              description = "The Nike Mercurial Superfly V CR7 Firm-Ground Football Boot provides exceptional ball touch and a lightweight, secure fit for speed on the pitch.",
              price = "$259.97", brand = brand1, user_id = 1)
session.add(Item1)
session.commit()

Item2 = Items(name = "NIKE MERCURIAL SUPERFLY V FG", image = "http://images.nike.com/is/image/DotCom/PDP_HERO/831940_408_A_PREM/mercurial-superfly-v-firm-ground-soccer-cleat.jpg",
              description = "The Nike Mercurial Superfly V Firm-Ground Soccer Cleat provides a perfect fit, exceptional ball touch and explosive traction for ultimate speed on short-grass fields.",
              price = "$300", brand = brand1, user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(name = "NIKE HYPERVENOM PHANTOM III DYNAMIC FIT FG", image = "http://images.nike.com/is/image/DotCom/PDP_COPY/905274_408/hypervenom-phantom-iii-dynamic-fit-firm-ground-soccer-cleat.jpg",
              description = "Designed for the for the attacking goalscorer, the Nike Hypervenom Phantom III Dynamic Fit Firm-Ground Soccer Cleat delivers a sock-like fit while increasing shot velocity and enabling quick changes of direction on short-grass fields.",
              price = "$300", brand = brand1, user_id=1)
session.add(Item3)
session.commit()

Item4 = Items(name = "NIKE TIEMPO LEGEND VI SG-PRO", image = "http://images.nike.com/is/image/DotCom/PDP_COPY/819680_103/tiempo-legend-vi-soft-ground-soccer-cleat.jpg",
              description = "The Nike Tiempo Legend VI Soft-Ground Soccer Cleat is designed for lightweight stability and precision control on wet and muddy fields, featuring a snug-fitting, tongueless construction and supple, water-repellent kangaroo leather.",
              price = "$210", brand = brand1, user_id=1)
session.add(Item4)
session.commit()

Item5 = Items(name = "NIKE MAGISTA OBRA II FG", image = "http://images.nike.com/is/image/DotCom/PDP_COPY/844595_409/magista-obra-ii-firm-ground-soccer-cleat.jpg",
              description = "The Nike Magista Obra II FG Firm-Ground Soccer Cleat provides precise touch and enhanced fit to help you perform playmaking moves on the field. Its firm-ground (FG) cleats are designed for use on short-grass fields that may be slightly wet but rarely muddy.",
              price = "$300", brand = brand1, user_id=1)
session.add(Item5)
session.commit()

Item6 = Items(name = "NIKE MERCURIALX PROXIMO II IC", image = "http://images.nike.com/is/image/DotCom/PDP_COPY/831976_005/mercurialx-proximo-ii-indoor-court-soccer-shoe.jpg",
              description = "The Nike MercurialX Proximo II Indoor/Court Soccer Shoe provides a perfect fit, exceptional ball touch and explosive traction for ultimate speed indoors and on the street",
              price = "$175", brand = brand1, user_id=1)
session.add(Item6)
session.commit()

#Adidas

brand2 = Brands(name = "Adidas", user_id=1)
session.add(brand2)
session.commit()

Item1 = Items(name = "ACE15.1 FG/AG BOOTS", image = "http://demandware.edgesuite.net/sits_pod14-adidas/dw/image/v2/aagl_prd/on/demandware.static/-/Sites-adidas-products/default/dw72c4286c/zoom/B32859_01_standard.jpg?sw=500&sfrm=jpg",
              description = "The game is changing, and it takes the player with complete control to create the plays, build up chances and finish them with clinical precision.",
              price = "$210", brand = brand2, user_id=1)
session.add(Item1)
session.commit()

Item2 = Items(name = "F10 FG MESSI BOOTS", image = "http://demandware.edgesuite.net/sits_pod14-adidas/dw/image/v2/aagl_prd/on/demandware.static/-/Sites-adidas-products/default/dw07e18fb2/zoom/M21764_01_standard.jpg?sw=500&sfrm=jpg",
              description = "These men's football boots will help you play with all the untouchable and unpredictable moves of Messi. Showing off an allover graphic inspired by the Argentine legend, they have a lightweight synthetic upper with a leather finish on the forefoot for a soft touch. Featuring the SPEEDTRAXION stud alignment for flat-out speed on firm ground.",
              price = "$299", brand = brand2, user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(name = "F50 ADIZERO FG", image = "http://demandware.edgesuite.net/sits_pod14-adidas/dw/image/v2/aagl_prd/on/demandware.static/-/Sites-adidas-products/default/dw7f8802eb/zoom/B34854_01_standard.jpg?sw=500&sfrm=jpg",
              description = "Possessed by speed, the all new F50 haunts the competition with allover 3D DRIBBLETEX for high-speed dribbling, wet or dry, a shimmer upper and an extra layer of studs on the translucent firm ground outsole.",
              price = "$249", brand = brand2, user_id=1)
session.add(Item3)
session.commit()

Item4 = Items(name = "F10 FG", image = "http://demandware.edgesuite.net/sits_pod14-adidas/dw/image/v2/aagl_prd/on/demandware.static/-/Sites-adidas-products/default/dw1c2d0ac9/zoom/B34859_01_standard.jpg?sw=500&sfrm=jpg",
              description = "The spirit of speed lives in this boot.",
              price = "$249", brand = brand2, user_id=1)
session.add(Item4)
session.commit()

Item5 = Items(name = "X15.1 FG/AG BOOTS", image = "http://demandware.edgesuite.net/sits_pod14-adidas/dw/image/v2/aagl_prd/on/demandware.static/-/Sites-adidas-products/default/dw32bd3ffb/zoom/B26978_01_standard.jpg?sw=500&sfrm=jpg",
              description = "It's the players you can't predict who change the game. The ones who pull chances out of nowhere. Who can't be caught because their opponents never know what they're going to do next. The creative playmakers who are always unmistakable and always unpredictable. ",
              price = "$299", brand = brand2, user_id=1)
session.add(Item5)
session.commit()


#Umbro

brand3 = Brands(name = "Umbro", user_id=1)
session.add(brand3)
session.commit()

Item1 = Items(name = "Medusae Pro HG Football Boots", image = "http://media.supercheapauto.com.au/sports/images/zooms/39530001-zoom.jpg",
              description = "Magic touch and lightning speed - two things that every players wants to have in their locker. The new Umbro Medusae Pro is a football boot which offers both thanks to an upper that combines premium k-leather on the forefoot with a lightweight performance mesh, making the Medusae one of the lightest leather boots on the market.",
              price = "$199", brand = brand3, user_id=1)
session.add(Item1)
session.commit()

Item2 = Items(name = "Velocita Pro HG Football Boots", image = "https://www.umbro.com/en-us/wp-content/uploads/sites/2/2017/01/Velocita-3-Main.png",
              description = "Don't Get Caught is the philosophy behind the Velocita, the latest evolution in Umbros speed boot silo. The new Velocita football boot offers comfort and fit through a special tri-layer construction on the upper, combined with an outsole designed to offer traction, agility and acceleration, to deliver a speed boot for people who don't just want to run in straight lines.",
              price = "$249", brand = brand3, user_id=1)
session.add(Item2)
session.commit()

Item3 = Items(name = "UX Accuro Pro HG Football Boots", image = "http://cdn.sportlaunches.com/wp-content/uploads/2017/04/Umbro-UX-Accuro-Pro-HG-Football-Boots.jpg",
              description = "Deadly Comfort unleashed! Umbro's new boot takes comfort to the next level with a host of features designed to add a deadly edge to your game.With a brand new 'pro-stance' outsole designed to give you balance and stability, the UX-Accuro Pro also features dedicated touch and strike zones on the upper to help you control, move and strike the ball.",
              price = "$249", brand = brand3, user_id=1)
session.add(Item3)
session.commit()

Item4 = Items(name = "Speciali Eternal Pro HG Football Boots", image = "http://www.thegaastore.com/Images/Models/Original/22746.jpg",
              description = "A classic returns! Reborn and ready for the modern game, the Speciali Eternal is inspired by the greatest boot in Umbro's history. The original Speciali is part of football history - worn by Shearer, Owen, Valderrama, Roberto Carlos and Pepe amongst many others - the boot has scored hundreds of goals and inspired thousands of memories. ",
              price = "$249", brand = brand3, user_id=1)
session.add(Item4)
session.commit()




print "added menu items!"
