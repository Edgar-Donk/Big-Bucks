============
Using Polars
============

When dealing with dataframes in Python the go to library has invariably been
Pandas. It is pretty ubiquitous, but when dealing with larger datasets it
starts to show its limitations. Firstly it is based on Numpy and for small to 
medium datasets it works well enough, but on larger datasets it starts to 
slow down and may not be able to load the data without breaking into chunks.

This is where Polars outshines Pandas, it is based on a combination of running
on Rust, using Arrow storage and ability to use a lazy method when required,
rather than the eager method used by Pandas. Along with a reworking of the methods
used, lazy working helps to speed up how quickly the result is processed.

It does mean that the whole approach may need revising, although there exist aids 
to assist conversion from Pandas. One problem is that being fairly new some
methods have been superceded so the internet sites date fairly quickly - obviously
testing is vital.

Using Polars for EDA
====================

Exploratory Data Analysis (EDA) are the initial steps used to query and understand
a dataframe. To tie this to a real life case we shall use the Starbucks location
dataframe, once the dataframe is mapped out we can use Altair to plot the locations
worldwide, as a country, state and city.

First make sure we can use Polars.

Install Polars
==============

We can install using pip or conda::

   $ pip install polars

or::

   $ conda install polars

Older Machines
--------------

Older computers may have a runtime warning::

	RuntimeWarning: Missing required CPU features.

	The following required CPU features were not detected:
    avx2, fma, bmi1, bmi2, lzcnt, movbe

	Continuing to use this version of Polars on this processor will likely 
	result in a crash.
	Install `polars[rtcompat]` instead of `polars` to run Polars with better compatibility.

	Hint: If you are on an Apple ARM machine (e.g. M1) this is likely due to running 
	Python under Rosetta.
	It is recommended to install a native version of Python that does not run under Rosetta 
	x86-64 emulation.

They require the following additional installation::

	$ pip install polars[rtcompat]

or::

	$ conda install polars[rtcompat] 
   
Lazy versus Eager Loading
=========================

Polars was recently delivered when most of the computers were multicore so it
was designed to work in parallel rather than sequentially. With smaller databases
it is in order to run eager loading, but for larger databases the lazy method
waits to process aggregation and selection before loading the relevant parts of the
database.

This means that we have two approaches in polars, we can read a dataset if it is small
or scan the dataset if large::

   >> df = pl.read_csv('sales.csv')          # Eager (immediate)
   >> df = pl.scan_csv('sales.csv')          # Lazy (deferred)

In contrast pandas is restricted to *read_csv*, the eager method.

The expression syntax allows the query optimizer to rationalise the code
and exclude unnecessary data. Where before we may have split the query into
several units it is better to chain all the query together for polars. 

To see the result after using the expressions use *collect()* this materialises 
the LazyFrame into a DataFrame. 

.. hint::   LazyFrame versus DataFrame

   - A LazyFrame processes instructions (select, filter and/or aggregate), 
   - A DataFrame shows or writes data.
   
Working with Polars and Altair
------------------------------

When working in polars any python GUI can be used - the code is shown in the
following as a block
with two chevrons at the line start to show a python input. Just under the input
the output is shown.

.. sidebar:: The Normal Convention is Three Chevrons

   If three chevrons are used sphinx will load the python input and show the result,
   however the dataframe is too big and cannot be processed directly in sphinx.

When visualising the data, using Altair, switch to Jupyter from the python GUI, 
the normal python GUIs
cannot always show the interactive plots. The code will be shown in a block without
any chevrons for the Python input. Directly following the code block sphinx will show
the resulting Altair plot. The Starbucks dataframe is normally too
large to work unaided in Altair, so before visualising Polars was used to restrict 
the size before plotting. 

Data Cleaning
=============                                                   

When encountering a new dataframe, after the preliminary data has been gathered and 
assessed, properties of the dataframe are gathered that directly affect data
cleansing. The importance of the various properties can only be found out when we 
know how the dataframe will be used. On larger dataframes visualisation may help
to highlight problem areas that need fixing or methods to work around the problem.

Load the Starbucks locations dataframe. There are several sources, we will use
one of the Github sources. 

.. sidebar::   Loading from Github

   If you have a new source in github, to import first navigate to the
   folder which contains the data, then click on the *raw* data button and copy 
   the URL address, which will show ``https:// raw.github~`` within the browser 
   address bar.

In this case ::

   https://raw.githubusercontent.com/mmcloughlin/starbucks/refs/heads/master/locations.json
   https://raw.githubusercontent.com/nsujay/Analysis-of-Starbucks-Worldwide-Stores/refs/heads/master/Starbucks_store_locations.csv
   https://raw.githubusercontent.com/chrismeller/StarbucksLocations/refs/heads/master/stores.csv
   https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv

 
Use the last one listed which seems to be a clone from kaggles store locations.
This can be loaded as an external file which is useful when working with jupyter, also
it loads in sphinx::

   >> import polars as pl
   >> q0 = (
       pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv')
   )
   >> df0 = q0.collect()
   >> df0
   
   shape: (25_600, 13)
   ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store     ┆ Store     ┆ Ownership ┆ … ┆ Phone     ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number    ┆ Name      ┆ Type      ┆   ┆ Number    ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str       ┆ str       ┆ str       ┆   ┆ str       ┆           ┆           ┆          │
   ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 47370-257 ┆ Meritxell ┆ Licensed  ┆ … ┆ 376818720 ┆ GMT+1:00  ┆ 1.53      ┆ 42.51    │
   │           ┆ 954       ┆ , 96      ┆           ┆   ┆           ┆ Europe/An ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ dorra     ┆           ┆          │
   │ Starbucks ┆ 22331-212 ┆ Ajman     ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 55.47     ┆ 25.42    │
   │           ┆ 325       ┆ Drive     ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆ Thru      ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ Starbucks ┆ 47089-256 ┆ Dana Mall ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 55.47     ┆ 25.39    │
   │           ┆ 771       ┆           ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ Starbucks ┆ 22126-218 ┆ Twofour   ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 54.38     ┆ 24.48    │
   │           ┆ 024       ┆ 54        ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ Starbucks ┆ 17127-178 ┆ Al Ain    ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 54.54     ┆ 24.51    │
   │           ┆ 586       ┆ Tower     ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …         ┆ …         ┆ …         ┆ …        │
   │ Starbucks ┆ 21401-212 ┆ Rex       ┆ Licensed  ┆ … ┆ 08 3824   ┆ GMT+00000 ┆ 106.7     ┆ 10.78    │
   │           ┆ 072       ┆           ┆           ┆   ┆ 4668      ┆ 0 Asia/Sa ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ igon      ┆           ┆          │
   │ Starbucks ┆ 24010-226 ┆ Panorama  ┆ Licensed  ┆ … ┆ 08 5413   ┆ GMT+00000 ┆ 106.71    ┆ 10.72    │
   │           ┆ 985       ┆           ┆           ┆   ┆ 8292      ┆ 0 Asia/Sa ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ igon      ┆           ┆          │
   │ Starbucks ┆ 47608-253 ┆ Rosebank  ┆ Licensed  ┆ … ┆ 278735001 ┆ GMT+00000 ┆ 28.04     ┆ -26.15   │
   │           ┆ 804       ┆ Mall      ┆           ┆   ┆ 59        ┆ 0 Africa/ ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ Johannesb ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ urg       ┆           ┆          │
   │ Starbucks ┆ 47640-253 ┆ Menlyn    ┆ Licensed  ┆ … ┆ null      ┆ GMT+00000 ┆ 28.28     ┆ -25.79   │
   │           ┆ 809       ┆ Maine     ┆           ┆   ┆           ┆ 0 Africa/ ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ Johannesb ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ urg       ┆           ┆          │
   │ Starbucks ┆ 47609-253 ┆ Mall of   ┆ Licensed  ┆ … ┆ 278735002 ┆ GMT+00000 ┆ 28.11     ┆ -26.02   │
   │           ┆ 286       ┆ Africa    ┆           ┆   ┆ 15        ┆ 0 Africa/ ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ Johannesb ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ urg       ┆           ┆          │
   └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
                                    
This shows we have a dataframe 25600 rows by 13 columns. Not all the columns were
shown, within LazyFrame we cannot use one of the polars *attributes* to obtain 
a more complete picture, first run *q.collect()* then the relevant *attribute* 
since we are showing data.

.. sidebar:: Lazy  and Eager Output

   *q0* is the output of LazyFrame after it has loaded the csv file and *df0*
   is the output after this has been collected into a dataframe. If there was any
   selection, filtering or aggregation then the LazyFrame output would become *q*
   and the dataframe *df*.

The scan was enclosed in brackets to allow further data questions::

   >> df0.glimpse()
   
   Rows: 25600
   Columns: 13
   $ Brand          <str> 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks', 'Starbucks'
   $ Store Number   <str> '47370-257954', '22331-212325', '47089-256771', '22126-218024', '17127-178586', '17688-182164', '18182-182165', '23359-229184', '30781-99022', '20423-205465'
   $ Store Name     <str> 'Meritxell, 96', 'Ajman Drive Thru', 'Dana Mall', 'Twofour 54', 'Al Ain Tower', 'Dalma Mall, Ground Floor', 'Dalma Mall, Level 1', 'Debenhams Yas Mall', 'Khalidiya Street', 'Eastern Mangroves'
   $ Ownership Type <str> 'Licensed', 'Licensed', 'Licensed', 'Licensed', 'Licensed', 'Licensed', 'Licensed', 'Licensed', 'Licensed', 'Licensed'
   $ Street Address <str> 'Av. Meritxell, 96', '1 Street 69, Al Jarf', 'Sheikh Khalifa Bin Zayed St.', 'Al Salam Street', 'Khaldiya Area, Abu Dhabi Island', 'Dalma Mall, Mussafah', 'Dalma Mall, Mussafah', 'Yas Island', 'Khalidiya St.', 'Al Salam Street, The Mangroves'
   $ City           <str> 'Andorra la Vella', 'Ajman', 'Ajman', 'Abu Dhabi', 'Abu Dhabi', 'Abu Dhabi', 'Abu Dhabi', 'Abu Dhabi', 'Abu Dhabi', 'Abu Dhabi'
   $ State/Province <str> '7', 'AJ', 'AJ', 'AZ', 'AZ', 'AZ', 'AZ', 'AZ', 'AZ', 'AZ'
   $ Country        <str> 'AD', 'AE', 'AE', 'AE', 'AE', 'AE', 'AE', 'AE', 'AE', 'AE'
   $ Postcode       <str> 'AD500', null, null, null, null, null, null, null, null, null
   $ Phone Number   <str> '376818720', null, null, null, null, null, null, null, '26670052', null
   $ Timezone       <str> 'GMT+1:00 Europe/Andorra', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Dubai', 'GMT+04:00 Asia/Muscat', 'GMT+04:00 Asia/Dubai'
   $ Longitude      <f64> 1.53, 55.47, 55.47, 54.38, 54.54, 54.49, 54.49, 54.61, 55.69, 54.38
   $ Latitude       <f64> 42.51, 25.42, 25.39, 24.48, 24.51, 24.4, 24.4, 24.46, 24.19, 24.48

*glimpse* had to be made using the dataframe *df0*, it will not work with the lazyframe *q0*.

Let's find the number of empty data entries in the first column *Brand*::

   >> q = (
       pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv').select(pl.col('Brand').is_null().sum())
   )

   >> df = q.collect()
   >> df

   shape: (1, 1)
   ┌───────┐
   │ Brand │
   │ ---   │
   │ u64   │
   ╞═══════╡
   │ 0     │
   └───────┘

But wait we can do better - let's use the LazyFrame more sensibly::

   >> q = q0.select(pl.col('Brand').is_null().sum()) 
   >> df = q.collect()
   >> df
   
   shape: (1, 1)
   ┌───────┐
   │ Brand │
   │ ---   │
   │ u64   │
   ╞═══════╡
   │ 0     │
   └───────┘   

With such a wide dataframe it is better to use a method that shows the nulls over 
all the columns::

   >> df0.null_count()
   
   shape: (1, 13)
   ┌───────┬────────┬────────────┬───────────┬───┬──────────────┬──────────┬───────────┬──────────┐
   │ Brand ┆ Store  ┆ Store Name ┆ Ownership ┆ … ┆ Phone Number ┆ Timezone ┆ Longitude ┆ Latitude │
   │ ---   ┆ Number ┆ ---        ┆ Type      ┆   ┆ ---          ┆ ---      ┆ ---       ┆ ---      │
   │ u64   ┆ ---    ┆ u64        ┆ ---       ┆   ┆ u64          ┆ u64      ┆ u64       ┆ u64      │
   │       ┆ u64    ┆            ┆ u64       ┆   ┆              ┆          ┆           ┆          │
   ╞═══════╪════════╪════════════╪═══════════╪═══╪══════════════╪══════════╪═══════════╪══════════╡
   │ 0     ┆ 0      ┆ 0          ┆ 0         ┆ … ┆ 6861         ┆ 0        ┆ 1         ┆ 1        │
   └───────┴────────┴────────────┴───────────┴───┴──────────────┴──────────┴───────────┴──────────┘

Once again the output was truncated and some of the columns are missing::

   >> for col in q0.collect(): print(f'{col.name} - {col.is_null().sum()}')
   
   Brand - 0
   Store Number - 0
   Store Name - 0
   Ownership Type - 0
   Street Address - 2
   City - 14
   State/Province - 0
   Country - 0
   Postcode - 1521
   Phone Number - 6861
   Timezone - 0
   Longitude - 1
   Latitude - 1

It looks like almost a full house apart from *Postcode* and *Phone Nomber*.
Since we are interested in the locations the two columns *Longitude* and
*Latitude* need to be inspected - are we talking of a single row or are the
missing values in two separate rows. Which column(s) hold unique values for 
every entry - the *Store Number* is a likely candidate, *Store Name* and
*Street Address* less likely.

.. sidebar:: Adding Python Code

   Beware of using python code such as this in normal queries, it will prevent 
   polars optimising. 

Better if we had used the inbuilt polars methods::

   >> q = (
       df0.select(pl.all().is_null().sum())
       .unpivot(value_name="missing")
       .filter(pl.col("missing") > 0)
   )
   >> missing = q.collect()

   >> print("Missing columns:")
   >> print(missing)
   
   Missing columns:
   shape: (6, 2)
   ┌────────────────┬─────────┐
   │ variable       ┆ missing │
   │ ---            ┆ ---     │
   │ str            ┆ u64     │
   ╞════════════════╪═════════╡
   │ Street Address ┆ 2       │
   │ City           ┆ 14      │
   │ Postcode       ┆ 1521    │
   │ Phone Number   ┆ 6861    │
   │ Longitude      ┆ 1       │
   │ Latitude       ┆ 1       │
   └────────────────┴─────────┘   
   
Check on *Store Name* to see how many unique values we have::

   >> q = q0.select("Store Name").unique().count()
   >> unique_types = q.collect()
   >> print(unique_types)
   
   shape: (1, 1)
   ┌────────────┐
   │ Store Name │
   │ ---        │
   │ u64        │
   ╞════════════╡
   │ 25364      │
   └────────────┘ 

There must be quite a few duplicates, 236.  

Also check on *Store Number* as opposed to *Store Name*::

   >> q = q0.select("Store Number").unique().count()
   
   >> q.collect()
   
   shape: (1, 1)
   ┌──────────────┐
   │ Store Number │
   │ ---          │
   │ u64          │
   ╞══════════════╡
   │ 25599        │
   └──────────────┘  

That shows we have one duplicate as there were no null values.
 
Are there any duplicated rows::
   
   >> df = q0.collect()
   >> (df
    .filter(df.is_duplicated())
    )
    
   shape: (0, 13)
   ┌───────┬────────┬────────────┬───────────┬───┬──────────────┬──────────┬───────────┬──────────┐
   │ Brand ┆ Store  ┆ Store Name ┆ Ownership ┆ … ┆ Phone Number ┆ Timezone ┆ Longitude ┆ Latitude │
   │ ---   ┆ Number ┆ ---        ┆ Type      ┆   ┆ ---          ┆ ---      ┆ ---       ┆ ---      │
   │ str   ┆ ---    ┆ str        ┆ ---       ┆   ┆ str          ┆ str      ┆ f64       ┆ f64      │
   │       ┆ str    ┆            ┆ str       ┆   ┆              ┆          ┆           ┆          │
   ╞═══════╪════════╪════════════╪═══════════╪═══╪══════════════╪══════════╪═══════════╪══════════╡
   └───────┴────────┴────────────┴───────────┴───┴──────────────┴──────────┴───────────┴──────────┘  

No row duplicates, one less problem.

.. sidebar:: Using df

   We had to use the Dataframe *df* as it is referred within the method,

Let's see what is happening in the rows where *Longitude* and *Latitude* are null::

   >> q = q0.filter(pl.col("Latitude").is_null())
   >> q.collect()
   
   shape: (1, 13)
   ┌───────────┬────────────┬────────────┬────────────┬───┬────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store      ┆ Store Name ┆ Ownership  ┆ … ┆ Phone  ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number     ┆ ---        ┆ Type       ┆   ┆ Number ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---        ┆ str        ┆ ---        ┆   ┆ ---    ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str        ┆            ┆ str        ┆   ┆ str    ┆           ┆           ┆          │
   ╞═══════════╪════════════╪════════════╪════════════╪═══╪════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 19773-1609 ┆ Yoido IFC  ┆ Joint      ┆ … ┆ null   ┆ GMT+09:00 ┆ null      ┆ null     │
   │           ┆ 73         ┆ Mall - 1F  ┆ Venture    ┆   ┆        ┆ Asia/Seou ┆           ┆          │
   │           ┆            ┆            ┆            ┆   ┆        ┆ l         ┆           ┆          │
   └───────────┴────────────┴────────────┴────────────┴───┴────────┴───────────┴───────────┴──────────┘

Both *Longitude* and *Latitude* are null in this row. We may be lucky and one of the
duplicated *Store Number* might just be this row-

In this instance the square brackets 
are necessary::

   >> (df0
       ['Store Number']
       .value_counts(sort=True)
       )
       
   shape: (25_599, 2)
   ┌──────────────┬───────┐
   │ Store Number ┆ count │
   │ ---          ┆ ---   │
   │ str          ┆ u64   │
   ╞══════════════╪═══════╡
   │ 19773-160973 ┆ 2     │
   │ 47370-257954 ┆ 1     │
   │ 22331-212325 ┆ 1     │
   │ 47089-256771 ┆ 1     │
   │ 22126-218024 ┆ 1     │
   │ …            ┆ …     │
   │ 21401-212072 ┆ 1     │
   │ 24010-226985 ┆ 1     │
   │ 47608-253804 ┆ 1     │
   │ 47640-253809 ┆ 1     │
   │ 47609-253286 ┆ 1     │
   └──────────────┴───────┘

.. sidebar::   Polars and Square Brackets

   Polars has been dropping the use of square brackets wherever possible - and
   using normal brackets instead.
   
It appears that our
Seoul store is the only one duplicated::

   >> q = q0.filter((pl.col("Store Number") == "19773-160973"))
   
   >> df = q.collect()
   
   >> df
   
   shape: (2, 13)
   ┌───────────┬────────────┬────────────┬────────────┬───┬────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store      ┆ Store Name ┆ Ownership  ┆ … ┆ Phone  ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number     ┆ ---        ┆ Type       ┆   ┆ Number ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---        ┆ str        ┆ ---        ┆   ┆ ---    ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str        ┆            ┆ str        ┆   ┆ str    ┆           ┆           ┆          │
   ╞═══════════╪════════════╪════════════╪════════════╪═══╪════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 19773-1609 ┆ Yoido IFC  ┆ Joint      ┆ … ┆ null   ┆ GMT+09:00 ┆ null      ┆ null     │
   │           ┆ 73         ┆ Mall - 1F  ┆ Venture    ┆   ┆        ┆ Asia/Seou ┆           ┆          │
   │           ┆            ┆            ┆            ┆   ┆        ┆ l         ┆           ┆          │
   │ Starbucks ┆ 19773-1609 ┆ Yoido IFC  ┆ Joint      ┆ … ┆ null   ┆ GMT+09:00 ┆ 126.92    ┆ 37.53    │
   │           ┆ 73         ┆ Mall - 1F  ┆ Venture    ┆   ┆        ┆ Asia/Seou ┆           ┆          │
   │           ┆            ┆            ┆            ┆   ┆        ┆ l         ┆           ┆          │
   └───────────┴────────────┴────────────┴────────────┴───┴────────┴───────────┴───────────┴──────────┘

Scroll to the end of the output, the second entry has *Longitude* and *Latitude* values
which seem to be correct for the Yoido IFC Mall, so we can delete the row with both
empty coordinates::

   >> df2 = df0.filter(pl.col("Longitude").is_not_null())
   >> print("DataFrame after dropping rows with nulls in 'Longitude':\n", df2)
   
   DataFrame after dropping rows with nulls in 'Longitude':
   
   shape: (25_599, 13)
   ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store     ┆ Store     ┆ Ownership ┆ … ┆ Phone     ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number    ┆ Name      ┆ Type      ┆   ┆ Number    ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str       ┆ str       ┆ str       ┆   ┆ str       ┆           ┆           ┆          │
   ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 47370-257 ┆ Meritxell ┆ Licensed  ┆ … ┆ 376818720 ┆ GMT+1:00  ┆ 1.53      ┆ 42.51    │
   │           ┆ 954       ┆ , 96      ┆           ┆   ┆           ┆ Europe/An ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ dorra     ┆           ┆          │
   │ Starbucks ┆ 22331-212 ┆ Ajman     ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 55.47     ┆ 25.42    │
   │           ┆ 325       ┆ Drive     ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆ Thru      ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ Starbucks ┆ 47089-256 ┆ Dana Mall ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 55.47     ┆ 25.39    │
   │           ┆ 771       ┆           ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ Starbucks ┆ 22126-218 ┆ Twofour   ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 54.38     ┆ 24.48    │
   │           ┆ 024       ┆ 54        ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ Starbucks ┆ 17127-178 ┆ Al Ain    ┆ Licensed  ┆ … ┆ null      ┆ GMT+04:00 ┆ 54.54     ┆ 24.51    │
   │           ┆ 586       ┆ Tower     ┆           ┆   ┆           ┆ Asia/Duba ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ i         ┆           ┆          │
   │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …         ┆ …         ┆ …         ┆ …        │
   │ Starbucks ┆ 21401-212 ┆ Rex       ┆ Licensed  ┆ … ┆ 08 3824   ┆ GMT+00000 ┆ 106.7     ┆ 10.78    │
   │           ┆ 072       ┆           ┆           ┆   ┆ 4668      ┆ 0 Asia/Sa ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ igon      ┆           ┆          │
   │ Starbucks ┆ 24010-226 ┆ Panorama  ┆ Licensed  ┆ … ┆ 08 5413   ┆ GMT+00000 ┆ 106.71    ┆ 10.72    │
   │           ┆ 985       ┆           ┆           ┆   ┆ 8292      ┆ 0 Asia/Sa ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ igon      ┆           ┆          │
   │ Starbucks ┆ 47608-253 ┆ Rosebank  ┆ Licensed  ┆ … ┆ 278735001 ┆ GMT+00000 ┆ 28.04     ┆ -26.15   │
   │           ┆ 804       ┆ Mall      ┆           ┆   ┆ 59        ┆ 0 Africa/ ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ Johannesb ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ urg       ┆           ┆          │
   │ Starbucks ┆ 47640-253 ┆ Menlyn    ┆ Licensed  ┆ … ┆ null      ┆ GMT+00000 ┆ 28.28     ┆ -25.79   │
   │           ┆ 809       ┆ Maine     ┆           ┆   ┆           ┆ 0 Africa/ ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ Johannesb ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ urg       ┆           ┆          │
   │ Starbucks ┆ 47609-253 ┆ Mall of   ┆ Licensed  ┆ … ┆ 278735002 ┆ GMT+00000 ┆ 28.11     ┆ -26.02   │
   │           ┆ 286       ┆ Africa    ┆           ┆   ┆ 15        ┆ 0 Africa/ ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ Johannesb ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ urg       ┆           ┆          │
   └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
 
We have one less row, recheck with the Store Number and df2 dataframe::
 
   >> df2.filter(
             pl.col("Store Number") == "19773-160973")
             
   shape: (1, 13)
   ┌───────────┬────────────┬────────────┬────────────┬───┬────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store      ┆ Store Name ┆ Ownership  ┆ … ┆ Phone  ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number     ┆ ---        ┆ Type       ┆   ┆ Number ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---        ┆ str        ┆ ---        ┆   ┆ ---    ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str        ┆            ┆ str        ┆   ┆ str    ┆           ┆           ┆          │
   ╞═══════════╪════════════╪════════════╪════════════╪═══╪════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 19773-1609 ┆ Yoido IFC  ┆ Joint      ┆ … ┆ null   ┆ GMT+09:00 ┆ 126.92    ┆ 37.53    │
   │           ┆ 73         ┆ Mall - 1F  ┆ Venture    ┆   ┆        ┆ Asia/Seou ┆           ┆          │
   │           ┆            ┆            ┆            ┆   ┆        ┆ l         ┆           ┆          │
   └───────────┴────────────┴────────────┴────────────┴───┴────────┴───────────┴───────────┴──────────┘

The *Longitude* and *Latitude* show their coordinates. That's a lot of scripts for just
one line of cleansing. With such a large dataframe it is unlikely to be able to
automate without losing a lot of data. There are many combinations, each requiring
a different solution. So if our Seoul data had been a single entry we would have 
loaded the coordinates - but there were two entries, so we had to find which one
had coordinates. If the empty cells had been split then we would have to load additional 
information to be able to retain the rows.

The majority of the dataframe is still unknown. This is where visualisation can help. 
*State/Province* and *Country* both seem complete, and we know that *Longitude* 
and *Latitude* are now complete.

Visualisation
=============

We can create a dataframe in Polars then use it in Altair. By adding a tooltip 
we can identify points on the chart - which in the following cases will be maps. 
It is 
important to reduce the number of points we are using, either by aggregation
or selecting one country, state or city at a time.

Let's first see how many different occurrences of the different columns
there are::

   >> (df2
          ['State/Province']
          .value_counts(sort=True)
          )
          
   shape: (338, 2)
   ┌────────────────┬───────┐
   │ State/Province ┆ count │
   │ ---            ┆ ---   │
   │ str            ┆ u64   │
   ╞════════════════╪═══════╡
   │ CA             ┆ 2821  │
   │ TX             ┆ 1042  │
   │ ENG            ┆ 787   │
   │ WA             ┆ 757   │
   │ 11             ┆ 705   │
   │ …              ┆ …     │
   │ POS            ┆ 1     │
   │ SFO            ┆ 1     │
   │ CYQ            ┆ 1     │
   │ TTT            ┆ 1     │
   │ TXQ            ┆ 1     │
   └────────────────┴───────┘

There are 338 distinct values for *State/Province*, California (CA) seems to be the
leader. Now let's see what *Country* shows::

   >> (df2
          ['Country']
          .value_counts(sort=True)
          )
          
   shape: (73, 2)
   ┌─────────┬───────┐
   │ Country ┆ count │
   │ ---     ┆ ---   │
   │ str     ┆ u64   │
   ╞═════════╪═══════╡
   │ US      ┆ 13608 │
   │ CN      ┆ 2734  │
   │ CA      ┆ 1468  │
   │ JP      ┆ 1237  │
   │ KR      ┆ 992   │
   │ …       ┆ …     │
   │ TT      ┆ 3     │
   │ ZA      ┆ 3     │
   │ LU      ┆ 2     │
   │ MC      ┆ 2     │
   │ AD      ┆ 1     │
   └─────────┴───────┘

There are only 73 countries, the majority of outlets concentrated into the US 
- just over half the total. China (CN) is in aecond place followed by Canada(CA).

If we were to use the country we would be stuck with a single
blob over the USA - not very useful unless we want to concentrate on the countries
outside the USA. Let's see what *City* shows::

   >> (df2
          ['City']
          .value_counts(sort=True)
          )
          
   shape: (5_471, 2)
   ┌──────────────┬───────┐
   │ City         ┆ count │
   │ ---          ┆ ---   │
   │ str          ┆ u64   │
   ╞══════════════╪═══════╡
   │ 上海市        ┆ 542   │
   │ Seoul        ┆ 242   │
   │ 北京市        ┆ 234   │
   │ New York     ┆ 232   │
   │ London       ┆ 216   │
   │ …            ┆ …     │
   │ Rock Springs ┆ 1     │
   │ Sheridian    ┆ 1     │
   │ Johannesburg ┆ 1     │
   │ Menlyn       ┆ 1     │
   │ Midrand      ┆ 1     │
   └──────────────┴───────┘
   
There are 5471 separate cities which would probably crowd out many
locations, the countries were too few but states appeared to be the best solution
we have - this will divide the US block into 50 states, which will be probably
manageable.

Aggregate on State/Province
---------------------------

Using polars, we are going to aggregate State/Province and provide the mean 
Latitude and Longitude, after the aggregation it should be safe to use altair.

Let's also show the number of stores per point, use *len()*, note
where this is positioned within *agg()*::

   >> q = (q0.group_by("State/Province")
      .agg(
                  pl.len().alias("count"),
                  pl.col("Longitude").mean(),
                  pl.col("Latitude").mean(),
               ) .sort("count", descending=True))
   >> df = q.collect()
   >> df
    shape: (338, 4)
   ┌────────────────┬───────┬─────────────┬───────────┐
   │ State/Province ┆ count ┆ Longitude   ┆ Latitude  │
   │ ---            ┆ ---   ┆ ---         ┆ ---       │
   │ str            ┆ u64   ┆ f64         ┆ f64       │
   ╞════════════════╪═══════╪═════════════╪═══════════╡
   │ CA             ┆ 2821  ┆ -119.505207 ┆ 35.510578 │
   │ TX             ┆ 1042  ┆ -97.100269  ┆ 31.092726 │
   │ ENG            ┆ 787   ┆ -1.012211   ┆ 52.163215 │
   │ WA             ┆ 757   ┆ -121.84465  ┆ 47.416618 │
   │ 11             ┆ 706   ┆ 121.629702  ┆ 37.964255 │
   │ …              ┆ …     ┆ …           ┆ …         │
   │ CAJ            ┆ 1     ┆ -78.51      ┆ -7.15     │
   │ YAR            ┆ 1     ┆ 39.87       ┆ 57.63     │
   │ TTT            ┆ 1     ┆ 121.15      ┆ 22.75     │
   │ IR             ┆ 1     ┆ 35.87       ┆ 32.58     │
   │ POS            ┆ 1     ┆ -61.53      ┆ 10.66     │
   └────────────────┴───────┴─────────────┴───────────┘ 

This produces 338 points, one for each State/Province, now first create a world map, 
available in altair, make this the background and superimpose the points made
with the df dataframe.

.. altair-plot::

   import polars as pl
   
   q0 = (
       pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv')
   )
   
   q = (q0.group_by("State/Province")
      .agg(
                  pl.len().alias("count"),
                  pl.col("Longitude").mean(),
                  pl.col("Latitude").mean(),
               ) .sort("count", descending=True))
   
   df = q.collect()
   
   import altair as alt
   from altair.datasets import data
      
   source = alt.topo_feature(data.world_110m.url, 'countries')
   
   background = alt.Chart(source).mark_geoshape(
       fill='lightgray',
       stroke='white'
   ).properties(
       width=500,
       height=300
   ).project('naturalEarth1')
      
   points = alt.Chart(df).mark_circle(
       color="tomato"
   ).encode(
       longitude="Longitude:Q", latitude="Latitude:Q",
       tooltip = ["State/Province", "count"]
   )
      
   background + points  
   
This will show tomato coloured points over the world map. Move your mouse pointer 
over the points and the State/Province is shown with their number. Most of the points seem to be located
in the correct place. Quite a few have strayed into the Atlantic, presumably pulled 
over by strays. This might be solved by adding *Country* to our group_by command::

   df2.group_by(['State/Province','Country']).agg(pl.len()).sort(['len'],descending=True)
   
   shape: (545, 3)
   State/Province	Country  len
   str            str      u64
   "CA"           "US"     2821
   "TX"           "US"     1042
   "ENG"          "GB"     787
   "WA"           "US"     757
   "FL"           "US"     694
   …              …        …
   "44"           "TH"     1
   "70"           "TH"     1
   "20"           "TR"     1
   "CHA"          "TT"     1
   "CYQ"          "TW"     1

This will increase the point number, so increase the map size.

.. altair-plot::

   q = (q0.group_by(("State/Province", "Country"))
   .agg(
               pl.len().alias("count"),
               pl.col("Longitude").mean(),
               pl.col("Latitude").mean(),
            ))
   
   df = q.collect()
   
   # alt.data_transformers.enable("vegafusion")
      
   source = alt.topo_feature(data.world_110m.url, 'countries')
   
   background = alt.Chart(source).mark_geoshape(
       fill='lightgray',
       stroke='white'
   ).properties(
       width=600,
       height=360
   ).project('naturalEarth1')
      
   points = alt.Chart(df).mark_circle(
       color="steelblue"
   ).encode(
       longitude="Longitude:Q", latitude="Latitude:Q",
       tooltip = ["State/Province", "Country", "count"]
   )
      
   background + points  

We added *Country* to the tooltip and changed the point colour.

Most of the obvious outlyers have disappeared. All the *State/Province* with numbers
seem to be in east Asia. If we add a *len()* we can find the count of each point
by adding *len* to the tooltip.

Some parts of the map are a continuous colour, to see what the situation is we
need to increase the map size country by country or reduce the number of points.-

As we have seen *State/Province* requires a major overhaul if used by itself. 

London Starbucks
================

If we wish to choose a city with an Altair map then London might fit the bill,
Altair has a map of greater London within its dataset collection showing the 
London boroughs::

   q = (
        pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv'
   ))
   
   q = q0.filter(
      (pl.col('City') == 'London') & (pl.col('Country') == 'GB'))
      
   q.collect()

   shape: (195, 13)
   ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store     ┆ Store     ┆ Ownership ┆ … ┆ Phone     ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number    ┆ Name      ┆ Type      ┆   ┆ Number    ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str       ┆ str       ┆ str       ┆   ┆ str       ┆           ┆           ┆          │
   ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 12929-137 ┆ Clapham - ┆ Company   ┆ … ┆ 207924467 ┆ GMT+0:00  ┆ -0.17     ┆ 51.46    │
   │           ┆ 795       ┆ St.       ┆ Owned     ┆   ┆ 0         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ John's    ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │           ┆           ┆ Road      ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 7013-1500 ┆ Brixton   ┆ Company   ┆ … ┆ 207274797 ┆ GMT+0:00  ┆ -0.11     ┆ 51.46    │
   │           ┆ 64        ┆ Station   ┆ Owned     ┆   ┆ 9         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │ Starbucks ┆ 14945-154 ┆ Stansted  ┆ Franchise ┆ … ┆ 01279     ┆ GMT+0:00  ┆ 0.25      ┆ 51.88    │
   │           ┆ 366       ┆ Airport   ┆           ┆   ┆ 680361    ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ DT        ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │ Starbucks ┆ 12949-140 ┆ Juxon     ┆ Company   ┆ … ┆ 207248035 ┆ GMT+0:00  ┆ -0.1      ┆ 51.51    │
   │           ┆ 506       ┆ House -   ┆ Owned     ┆   ┆ 9         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ St. Pauls ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │           ┆           ┆ Church…   ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 12600-982 ┆ Pentonvil ┆ Company   ┆ … ┆ 207812107 ┆ GMT+0:00  ┆ -0.12     ┆ 51.53    │
   │           ┆ 09        ┆ le Road   ┆ Owned     ┆   ┆ 3         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …         ┆ …         ┆ …         ┆ …        │
   │ Starbucks ┆ 12364-774 ┆ Oxford    ┆ Company   ┆ … ┆ 207491946 ┆ GMT+0:00  ┆ -0.15     ┆ 51.51    │
   │           ┆ 60        ┆ Street -  ┆ Owned     ┆   ┆ 3         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ Selfridge ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │           ┆           ┆ s         ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 1304-1438 ┆ Conduit   ┆ Company   ┆ … ┆ 207493975 ┆ GMT+0:00  ┆ -0.14     ┆ 51.51    │
   │           ┆ 65        ┆ Street    ┆ Owned     ┆   ┆ 4         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │ Starbucks ┆ 12397-856 ┆ Chiswick  ┆ Company   ┆ … ┆ 208994159 ┆ GMT+0:00  ┆ -0.26     ┆ 51.49    │
   │           ┆ 93        ┆ - High    ┆ Owned     ┆   ┆ 8         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ Road/Fish ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │           ┆           ┆ er's …    ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 12101-119 ┆ Covent    ┆ Company   ┆ … ┆ 207836623 ┆ GMT+0:00  ┆ -0.12     ┆ 51.51    │
   │           ┆ 03        ┆ Garden -  ┆ Owned     ┆   ┆ 1         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ Russell   ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │           ┆           ┆ St        ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 47901-260 ┆ London    ┆ Company   ┆ … ┆ 207407736 ┆ GMT+0:00  ┆ -0.09     ┆ 51.51    │
   │           ┆ 029       ┆ Bridge-Sh ┆ Owned     ┆   ┆ 4         ┆ Europe/Lo ┆           ┆          │
   │           ┆           ┆ ard       ┆           ┆   ┆           ┆ ndon      ┆           ┆          │
   │           ┆           ┆ Arcade    ┆           ┆   ┆           ┆           ┆           ┆          │
   └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘
   
Note that we added `('Country') == 'GB'` to ensure that no other London is included. `
We should be able to show 195 points on a London map.
 
.. altair-plot::

   import polars as pl
   import altair as alt
   from altair.datasets import data
   
   q0 = (
        pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv'
   ))
   
   q = q0.filter(
      (pl.col('City') == 'London') & (pl.col('Country') == 'GB'))
   
   df = q.collect()

   boroughs = alt.topo_feature(data.london_boroughs.url, 'boroughs')

   boroughs = alt.Chart(boroughs, width=700, height=500).mark_geoshape(
      stroke='white',
      strokeWidth=2
   ).encode(
      color=alt.value('#ccc'),
   )
   
   boroughs

Now add the London Starbucks.

.. altair-plot::

   London  = alt.Chart(df).mark_circle(
       color="tomato"
   ).encode(
       longitude="Longitude:Q", latitude="Latitude:Q", 
       tooltip = ["State/Province", "City", "Country", "Store Name"]
   )
   
   boroughs + London  

Adding the London Starbucks locations to the London map we find that the majority 
of locations are at the bottom
of the map, one location is at the top about a third of the way towards the centre 
- which shows as Victoria Station - one at Stanstead
airport - well outside the borough map - one at Borehamwood - in the home counties,
but maybe within the boroughs map.

First Victoria Station needs new coordinates and Stanstead airport can be dropped.
Victoria Station's existing coordinates put it well away from other coordinates, so
update using a *when, then, otherwise* method. Victoria Station is at Longitude -0.1441
and Latitude 51.4952, a far cry from the original::

   df = df.with_columns(
       pl.when(pl.col("Longitude") == -2.87).then(-0.1441).otherwise(pl.col("Longitude")).alias("Longitude")
   )
   
   df = df.with_columns(
       pl.when(pl.col("Latitude") == 55.74).then(51.4952).otherwise(pl.col("Latitude")).alias("Latitude")
   )
   
Dropping Stansted Airport was more difficult because the *Store Name* showed up as
``Stansted Airport DT`` on the tooltip - trying to use the *Store Name* failed with
"Stansted Airport DT" and "Stansted Airport DT " - going back to the coordinates
using Longitude 0.25 showed that the *Store Name* was ::

    "Stansted
   Airport DT"
   
   df.filter(pl.col("Longitude") == 0.25)
   
   shape: (1, 13)
   Brand       Store Number   Store Name  Ownership Type Street Address                   City     State/Province  Country  Postcode   Phone Number   Timezone                   Longitude   Latitude
   str         str            str         str            str                              str      str             str      str        str            str                        f64         f64
   "Starbucks" "14945-154366" "Stansted   "Franchise"    "A120 Thermal Lane, London Stan…"London"  "ENG"           "GB"     "CM24 1PY" "01279 680361" "GMT+0:00 Europe/London"   0.25        51.88
                               Airport DT"

We can drop Stansted using Longitude.

.. altair-plot::

   df = df.with_columns(
       pl.when(pl.col("Longitude") == -2.87).then(-0.1441).otherwise(pl.col("Longitude")).alias("Longitude")
   )
   
   df = df.with_columns(
       pl.when(pl.col("Latitude") == 55.74).then(51.4952).otherwise(pl.col("Latitude")).alias("Latitude")
   ) 

   df = df.filter(pl.col("Longitude") != 0.25)

   London  = alt.Chart(df).mark_circle(
       color="tomato"
   ).encode(
       longitude="Longitude:Q", latitude="Latitude:Q", 
       tooltip = ["State/Province", "City", "Country", "Store Name"]
   )
   
   boroughs + London   

This now showed the locations in the general outline of the London Boroughs, 
if necessary we could add the borough names to the map. Noticeable is the fact
that the coordinates have been massaged, there is no way that the stores appear
in straight rows, certainly not in London. To add the borough names we can use 
the Altair dataset *london_centroids* which gives the name and the centroid coordinates
for each London borough. *london_centroids* is a small database, it can be queried 
directly in altair::

   data.london_centroids().info()
   
   <class 'pandas.core.frame.DataFrame'>
   RangeIndex: 33 entries, 0 to 32
   Data columns (total 3 columns):
    #   Column  Non-Null Count  Dtype  
   ---  ------  --------------  -----  
    0   name    33 non-null     string 
    1   cx      33 non-null     Float64
    2   cy      33 non-null     Float64
   dtypes: Float64(2), string(1)
   memory usage: 990.0 bytes 

Note how the borough names are positioned.

.. altair-plot::

   centroids = data.london_centroids.url
   
   labels = alt.Chart(centroids).mark_text().encode(
       longitude='cx:Q',
       latitude='cy:Q',
       text='bLabel:N',
       size=alt.value(8),
       opacity=alt.value(0.8)
   ).transform_calculate(
       "bLabel", "indexof (datum.name,' ') > 0  ? substring(datum.name,0,indexof(datum.name, ' ')) : datum.name"
   )

   boroughs + labels

This looks well enough, now all together.

.. altair-plot::

   boroughs + labels + London   
 
We spotted Victoria Station required new coordinates, one in 195 rows, which over
25600 rows is probably amounting to about 130 poorly made coordinates, plus a column
*State/Province* poorly attributed or not clearly controlled. Unfortunately we 
cannot use the *Store Number* to help, as seen on the London Starbucks, the numbers
are probably allocated sequentially on a date basis, certainly not according to
*Country*, *State/Province* or *City*.

Empty City
==========

When we inirially looked at the data within the column *City* there were 14 
missing data entries in *City*.
Maybe we will be lucky and be able to find the *City* from the empty *City* - 
anyway worth a look::

   >> q = q0.filter(pl.col("City").is_null())
   >> q.collect()
   
   shape: (14, 13)
   ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store     ┆ Store     ┆ Ownership ┆ … ┆ Phone     ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number    ┆ Name      ┆ Type      ┆   ┆ Number    ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str       ┆ str       ┆ str       ┆   ┆ str       ┆           ┆           ┆          │
   ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 31657-104 ┆ سان       ┆ Licensed  ┆ … ┆ 201208002 ┆ GMT+2:00  ┆ 29.96     ┆ 31.24    │
   │           ┆ 436       ┆ ستيفانو   ┆           ┆   ┆ 87        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 32152-109 ┆ النايل    ┆ Licensed  ┆ … ┆ 201208003 ┆ GMT+2:00  ┆ 31.23     ┆ 30.07    │
   │           ┆ 504       ┆ سيتى      ┆           ┆   ┆ 07        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 32314-115 ┆ أسكندرية  ┆ Licensed  ┆ … ┆ 201850222 ┆ GMT+2:00  ┆ 31.03     ┆ 30.06    │
   │           ┆ 172       ┆ الصحراوى  ┆           ┆   ┆ 14        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 31479-105 ┆ مكرم عبيد ┆ Licensed  ┆ … ┆ 201208003 ┆ GMT+2:00  ┆ 31.34     ┆ 30.09    │
   │           ┆ 246       ┆           ┆           ┆   ┆ 32        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 31756-107 ┆ سيتى      ┆ Licensed  ┆ … ┆ 201208003 ┆ GMT+2:00  ┆ 31.33     ┆ 30.06    │
   │           ┆ 161       ┆ ستارز 1   ┆           ┆   ┆ 50        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …         ┆ …         ┆ …         ┆ …        │
   │ Starbucks ┆ 31646-106 ┆ مطار      ┆ Licensed  ┆ … ┆ 201208003 ┆ GMT+2:00  ┆ 31.41     ┆ 30.11    │
   │           ┆ 547       ┆ القاهرة   ┆           ┆   ┆ 35        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 31755-107 ┆ سنافير -  ┆ Licensed  ┆ … ┆ 201208003 ┆ GMT+2:00  ┆ 34.33     ┆ 27.91    │
   │           ┆ 182       ┆ نعمه بيه  ┆           ┆   ┆ 27        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 32389-107 ┆ المركاتو  ┆ Licensed  ┆ … ┆ 201850222 ┆ GMT+2:00  ┆ 34.33     ┆ 27.92    │
   │           ┆ 342       ┆ مول2      ┆           ┆   ┆ 17        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 32490-111 ┆ خان لاجونا ┆ Licensed  ┆ … ┆ 201898885 ┆ GMT+2:00  ┆ 34.43     ┆ 28.04    │
   │           ┆ 349       ┆           ┆           ┆   ┆ 47        ┆ Africa/Ca ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ iro       ┆           ┆          │
   │ Starbucks ┆ 31429-102 ┆ ابراج     ┆ Licensed  ┆ … ┆ 966257190 ┆ GMT+03:00 ┆ 39.83     ┆ 21.42    │
   │           ┆ 231       ┆ البيت 1   ┆           ┆   ┆ 12        ┆ Asia/Riya ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ dh        ┆           ┆          │
   └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘

Interesting the *Store Name* all had a similar script and the *Timezone* was Cairo.
Cairo is 31.23 longitude and 30.03 latitude - not so far from some of our empty *City*.
First check what the *Country* is::

   >> q = q0.filter(pl.col("City").is_null()).select(["Country"]) 
   >> pl.Config.set_tbl_rows(20)
   
   >> q.collect()
   shape: (14, 1)
   ┌─────────┐
   │ Country │
   │ ---     │
   │ str     │
   ╞═════════╡
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ EG      │
   │ SA      │
   └─────────┘  

One store was from Saudi Arabia (SA), the rest were Egypt (EG).

Let's see how it plots.

.. altair-plot::

   import polars as pl
   import altair as alt
   
   q0 = (
       pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv')
   )
   
   q = q0.filter(
      ( (pl.col('Country') == 'EG')))
   df = q.collect()
   
   url = "https://raw.githubusercontent.com/samateja/D3topoJson/refs/heads/master/egypt.json"
   
   source = alt.topo_feature(url, "egypt")
   
   eg = alt.Chart(source, width=700, height=500).mark_geoshape().encode()
   
   star  = alt.Chart(df).mark_circle(
       color="darkorange"
   ).encode(
       longitude="Longitude:Q", latitude="Latitude:Q",
       tooltip = ["Store Number", "State/Province", "City", "Country", "Store Name", "Street Address"]
   )
   
   eg + star
   
Not too bad, there is one stray Cairo plot on the north coast next to the Alexandria
entry. Two appear to be at Sharm El-Sheikh, the rest are concentrated at Cairo.
The two at Sharm El-Sheikh both are null for the *City*. As my Arabic is non-existant
we'll leave as is, maybe the one labelled *Cairo* on the Mediteranean is on the 
Cairo-Alexander Road about 28km from the Cairo centre.
   

Rhode Island Starbucks
======================

Check what is potting with the US states - let's choose Rhode Island it's small by 
American standards::

   >>import polars as pl
   >> q0 = (
       pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv')
   )
   >> q = q0.filter(
        (pl.col('State/Province') == 'RI') )
   >> q.collect()
   
   shape: (29, 13)
   
   ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store     ┆ Store     ┆ Ownership ┆ … ┆ Phone     ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number    ┆ Name      ┆ Type      ┆   ┆ Number    ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str       ┆ str       ┆ str       ┆   ┆ str       ┆           ┆           ┆          │
   ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 15755-164 ┆ Megamall  ┆ Licensed  ┆ … ┆ null      ┆ GMT+00000 ┆ 104.06    ┆ 1.13     │
   │           ┆ 624       ┆ Batam     ┆           ┆   ┆           ┆ 0 Asia/Ma ┆           ┆          │
   │           ┆           ┆ Center    ┆           ┆   ┆           ┆ kassar    ┆           ┆          │
   │ Starbucks ┆ 15756-164 ┆ Hang      ┆ Licensed  ┆ … ┆ null      ┆ GMT+07:00 ┆ 106.93    ┆ -6.22    │
   │           ┆ 625       ┆ Nadim     ┆           ┆   ┆           ┆ Asia/Jaka ┆           ┆          │
   │           ┆           ┆ Intl      ┆           ┆   ┆           ┆ rta       ┆           ┆          │
   │           ┆           ┆ Airport - ┆           ┆   ┆           ┆           ┆           ┆          │
   │           ┆           ┆ BTH       ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 7272-763  ┆ The Barri ┆ Company   ┆ … ┆ (401)     ┆ GMT-05:00 ┆ -71.3     ┆ 41.74    │
   │           ┆           ┆ ngton     ┆ Owned     ┆   ┆ 247-4687  ┆ America/N ┆           ┆          │
   │           ┆           ┆ Shopping  ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │           ┆           ┆ Center    ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 7355-1046 ┆ Garden    ┆ Company   ┆ … ┆ (401)     ┆ GMT-05:00 ┆ -71.46    ┆ 41.76    │
   │           ┆           ┆ City-Cran ┆ Owned     ┆   ┆ 464-8235  ┆ America/N ┆           ┆          │
   │           ┆           ┆ ston      ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │ Starbucks ┆ 7678-3784 ┆ East Gree ┆ Company   ┆ … ┆ 401-885-1 ┆ GMT-05:00 ┆ -71.45    ┆ 41.66    │
   │           ┆ 0         ┆ nwich/Mai ┆ Owned     ┆   ┆ 291       ┆ America/N ┆           ┆          │
   │           ┆           ┆ n St      ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …         ┆ …         ┆ …         ┆ …        │
   │ Starbucks ┆ 15660-156 ┆ Macy's    ┆ Licensed  ┆ … ┆ 401-468-3 ┆ GMT-05:00 ┆ -71.48    ┆ 41.72    │
   │           ┆ 764       ┆ Warwick   ┆           ┆   ┆ 778       ┆ America/N ┆           ┆          │
   │           ┆           ┆ Mall #39  ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │ Starbucks ┆ 7430-942  ┆ Warwick-B ┆ Company   ┆ … ┆ 401-823-9 ┆ GMT-05:00 ┆ -71.5     ┆ 41.7     │
   │           ┆           ┆ aldhill   ┆ Owned     ┆   ┆ 645       ┆ America/N ┆           ┆          │
   │           ┆           ┆ Rd.       ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │ Starbucks ┆ 76938-129 ┆ Target    ┆ Licensed  ┆ … ┆ (401)     ┆ GMT-05:00 ┆ -71.48    ┆ 41.72    │
   │           ┆ 827       ┆ Warwick   ┆           ┆   ┆ 244-1972  ┆ America/N ┆           ┆          │
   │           ┆           ┆ North     ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │           ┆           ┆ T-2430    ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 78039-112 ┆ PVD Main  ┆ Licensed  ┆ … ┆ 401-732-5 ┆ GMT-05:00 ┆ -71.44    ┆ 41.73    │
   │           ┆ 125       ┆ Food      ┆           ┆   ┆ 040       ┆ America/N ┆           ┆          │
   │           ┆           ┆ Court     ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   │ Starbucks ┆ 78027-112 ┆ PVD       ┆ Licensed  ┆ … ┆ 401-732-5 ┆ GMT-05:00 ┆ -71.44    ┆ 41.73    │
   │           ┆ 124       ┆ Baggage   ┆           ┆   ┆ 140       ┆ America/N ┆           ┆          │
   │           ┆           ┆ Claim     ┆           ┆   ┆           ┆ ew_York   ┆           ┆          │
   └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘

We have 29 outlets attributed to RI (Rhode Island) in the USA, let's see how they plot
on a map, there was no altair map at a large enough scale so we imported a map
which happens to be a GeoJson type. Hover over the points.

.. altair-plot::

   import altair as alt
   import polars as pl
   
   q0 = (
      pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv')
   )
   
   q = q0.filter(
        (pl.col('State/Province') == 'RI') )
   df = q.collect()

   url_geojson = 'https://raw.githubusercontent.com/khalid-alali/geojson/refs/heads/master/ri_rhode_island_zip_codes_geo.min.json'
   data_geojson_remote = alt.Data(url=url_geojson, format=alt.DataFormat(property='features',type='json'))
   # chart object
   map = alt.Chart(data_geojson_remote, width=700, height=500).mark_geoshape(
   stroke='white',
   strokeWidth=2).encode(
   color=alt.value('#ccc'),
   ).project(
   type='identity', reflectY=True) 
   
   Rhode  = alt.Chart(df).mark_circle(
      color="tomato"
   ).encode(
      longitude="Longitude:Q", latitude="Latitude:Q",
      tooltip = ["Store Number", "Store Name", "State/Province", "City", "Country", "Store Name","Longitude", "Latitude"]
   )

   map + Rhode 
   
You should see a blank map with three points, the two on the right are obviously
from somewhere else - the coordinates are nowhere near Rhode Island - they both 
come from Batam in Indonesia in the Riau Islands - hence the RI State.

Because there were do few points it was perfectly alright to use all the columns -
hence the large tooltip.

The third is at the Rhode Island TF Green Int'l Airport, which should be alright.
We can restrict the Rhode Island selection by adding the US as the country.

.. altair-plot::

   q = q0.filter(
        (pl.col('State/Province') == 'RI') & (pl.col('Country') == 'US'))
   df = q.collect()

   Rhode  = alt.Chart(df).mark_circle(
      color="tomato"
   ).encode(
      longitude="Longitude:Q", latitude="Latitude:Q",
      tooltip = ["Store Number", "Store Name", "State/Province", "City", "Country", "Store Name","Longitude", "Latitude"]
   )

   map + Rhode 
   
This appears to be what we want, there are now 27 outlets on our map, there is 
a group at Providence, the state capital, all the rest are single points. Our
baggage reclaim is some way away from the main airport buildings. Otherwise the
positions seem alright but could be checked more thoroughly if required.

Altair can import external files to generate a map, but the type has to be determined,
also if the map has multiple layers the layer or feature has to be declared.

Belgium Starbucks
=================

Let's see what happens with a country, such as Belgium, mostly because there is
a TopoJSON map in Github which loads. Rhode Island was mapped by geoJson and 
required inverting together with type *identity* to straighten it up. 

The country code for Belgium is *BE*::

   >> import polars as pl

   q0 = (
        pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv'
   ))
   
   q = q0.filter(
      ( (pl.col('Country') == 'BE')))
   df = q.collect()
      
   df
   shape: (19, 13)
   
   ┌───────────┬───────────┬───────────┬───────────┬───┬───────────┬───────────┬───────────┬──────────┐
   │ Brand     ┆ Store     ┆ Store     ┆ Ownership ┆ … ┆ Phone     ┆ Timezone  ┆ Longitude ┆ Latitude │
   │ ---       ┆ Number    ┆ Name      ┆ Type      ┆   ┆ Number    ┆ ---       ┆ ---       ┆ ---      │
   │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ ---       ┆ str       ┆ f64       ┆ f64      │
   │           ┆ str       ┆ str       ┆ str       ┆   ┆ str       ┆           ┆           ┆          │
   ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪═══════════╪═══════════╪═══════════╪══════════╡
   │ Starbucks ┆ 48462-260 ┆ Brussels  ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.38      ┆ 50.84    │
   │           ┆ 556       ┆ Schuman   ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Metro     ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │           ┆           ┆ Station   ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 26401-240 ┆ Brussels  ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.35      ┆ 50.83    │
   │           ┆ 667       ┆ Louise    ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Metro     ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │           ┆           ┆ Station   ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 26399-240 ┆ Brussels  ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.33      ┆ 50.83    │
   │           ┆ 668       ┆ - Gare du ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Midi (M)  ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │ Starbucks ┆ 48459-260 ┆ Brussels  ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.41      ┆ 50.84    │
   │           ┆ 557       ┆ Metro     ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Station   ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │ Starbucks ┆ 18497-185 ┆ Antwerp   ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.4       ┆ 51.22    │
   │           ┆ 504       ┆ Groenplaa ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ ts        ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …         ┆ …         ┆ …         ┆ …        │
   │ Starbucks ┆ 32639-137 ┆ Brussels  ┆ Licensed  ┆ … ┆ +32 2 719 ┆ GMT+1:00  ┆ 4.49      ┆ 50.9     │
   │           ┆ 287       ┆ Airport   ┆           ┆   ┆ 77 00     ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Depart.   ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │           ┆           ┆ Hall      ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 1338-2459 ┆ Brussels  ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.48      ┆ 50.87    │
   │           ┆ 53        ┆ Airport   ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Concourse ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │           ┆           ┆ A         ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 6030-1372 ┆ Brussels  ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.48      ┆ 50.9     │
   │           ┆ 90        ┆ Airport   ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Concourse ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │           ┆           ┆ B         ┆           ┆   ┆           ┆           ┆           ┆          │
   │ Starbucks ┆ 28830-248 ┆ Liege Gui ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 5.57      ┆ 50.63    │
   │           ┆ 724       ┆ llemins   ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆ Station   ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   │ Starbucks ┆ 19372-201 ┆ Gare de   ┆ Licensed  ┆ … ┆ null      ┆ GMT+1:00  ┆ 4.86      ┆ 50.47    │
   │           ┆ 645       ┆ Namur     ┆           ┆   ┆           ┆ Europe/Br ┆           ┆          │
   │           ┆           ┆           ┆           ┆   ┆           ┆ ussels    ┆           ┆          │
   └───────────┴───────────┴───────────┴───────────┴───┴───────────┴───────────┴───────────┴──────────┘

We have only 19 outlets.

The source Bart Mesuere kindly showed that the feature we need is *municipalities*, 
he also stated not to use the properties part but the geo-part is good.

.. altair-plot::

   import altair as alt
   
   url = "https://raw.githubusercontent.com/bmesuere/belgium-topojson/refs/heads/master/belgium.json"

   source = alt.topo_feature(url, "municipalities")

   be = alt.Chart(source, width=700, height=500).mark_geoshape().encode()
   
   be
   
It seems to load without any great fuss, we are leaving the map as just the country
plot without any provincial boundaries. 

.. altair-plot::

   import polars as pl

   q0 = (
        pl.scan_csv('https://raw.githubusercontent.com/sunny2309/datasets/refs/heads/master/starbucks_store_locations.csv'
   ))
   
   q = q0.filter(
      ( (pl.col('Country') == 'BE')))
   df = q.collect()   

   star  = alt.Chart(df).mark_circle(
       color="darkorange"
   ).encode(
       longitude="Longitude:Q", latitude="Latitude:Q",
       tooltip = ["State/Province", "City", "Country", "Store Name"]
   )
   
   be + star

The plot should show a few single outlets at the larger towns and a small crowd at
Brussels. No outlyers were apparent. It seems when working with country codes 
we are less likely
to have outlets from other lands sharing the same code.

Provided we can find a TopoJSON that plots it is easier working with this format
when plotting.

That was rather tame - more interesting would be to look at one of the outlyers
found on the world map when using *State/Province*.

