# YOLO model tanítás - 2025.02.07

## Kézi annotálás, első model tanítás és tesztelése

### 1.
A ```#1015159``` task-on 200 képet felannotáltam manuálisan, erre készítettem egy kezdetleges betanítást, amit később ugyanezen a taskon az 500+ adathalmazon teszteltem. A model által elvégzett annotálások nem voltak vészesek, de több helyen nem ismert fel sejteket, illetve mivel 8 esetből tanulta az osztódást így szinte elenyésző esetben sikerült neki érdemleges osztódást annotálnia. Ez egyből a tanítás után jelentkezett is az adatokból, hogy kevés osztódási példája volt.

### 2.
A ```#1015159``` task-on és adathalmazon (500+ kép) futattott model hibáit javítottam továbbra is manuális, végig a teljes adathalmazon. Így sikerült több újabb sejt eseteket jelölnöm és több helyes osztódást is.

**PROBLÉMA:** Nem minden esetben tudom eldönteni, hogy az valóban sejt a képen vagy egyéb "anyag".

## Második model tanítása nagyobb adathalmazból

### 1.
Az új modelt az előző task adathalmazából újratanítottam, közben finomítottam a tanulás beállításain, illetve igazodtam ahhoz, hogy nagyobb adathalmaz, több erőforrás, több idő.

**BEÁLLÍTÁSOK:**
```python
model = YOLO('yolov8l.pt')
model.train(data="data.yaml", epochs=75, imgsz=832, batch=8, device=device, augment=True)
```

```yaml
path: /content/drive/MyDrive/dataset
train: images/train
val: images/val
nc: 2
names: ['cell', 'division']

augment:
  mosaic: 0.1
  mixup: 0.1
  hsv_h: 0.01
  hsv_s: 0.4
  hsv_v: 0.2
  perspective: 0.05
  flipud: 0.2
  fliplr: 0.2
```

Az új beállításokban törekedtem arra, hogy a tanítás folyamán több, eltérő esetet is kapjon így **Augment** mellett döntöttem (pontosan még nem tudom, hogy mik a legjobb beállítások, a közeljövőben és a következő tanításokkor mindenképp pontosabb beállítást szeretnék).
Utólag talán növelhettem volna az epoch számot, de nem szerettem volna, hogy **overfitting** következzen be.
Sajnos mivel erőforrásban korlátozott vagyok így a Google Colab szolgáltatást vettem igénybe, de ott is csak bizonyos határokig tudok elmenni.

**TANULÁS EREDMÉNYE:**
!["result"](/trains/2025-02-07/images/last_train_result.png)

## Második model tesztelése

Az elkészült modelt a ```#1015150``` task adathalmazán (1588 kép) teszteltem le. Az eredménnyel nem vagyok teljesen megelégedve, azonban a tanult sejttípusokat (nem osztódás) sok esetben felismerte. Azonban ebben az adathalmazban sok új eset is van, mind sejt és osztódás terén is, így mindenképp foglalkozni kell az annotálások manuális javításával.

**ANNOTÁLÁS EREDMÉNYEK:**
!["example_1"](/trains/2025-02-07/images/example_1.png)
Nem ismerte fel az összes sejtet.

!["example_2"](/trains/2025-02-07/images/example_2.png)
Nem ismerte fel az összes sejtet és az osztódást.

!["example_3"](/trains/2025-02-07/images/example_3.png)
Pozitívum, hogy szinte az összeset sejtet felismerte.

## Következtetés

- Kisebb adathalmazból haladva a nagy adathalmazig szükséges pontosabb annotálások manuálisan a tanításhoz.
- A tanítás beállításait még finomhangolni kell a jobb teljesítményhez.
- Az utolsó tesztelés során a nagy adathalmazban keletkezett hiányos/téves annotálások javítása a közeljövőben a pontosabb eredményekhez.