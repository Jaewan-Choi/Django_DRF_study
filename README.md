# ✔️ 장고 DRF 과제

## 1. *args, **kwargs 예제 코드

```py
# a, b : 고정적으로 받는 변수(없으면 에러)
# *args, **kwargs : 없어도 상관없음
def numbers(a, b, *args, **kwargs):
    print(f"{a, b}")
    >> (1, 2)
    
    print(f"{a, b, args}")
    >> (1, 2, (3, 4))  # 튜플로 출력
    
    print(f"{a, b, args, kwargs}")
    >> (1, 2, (3, 4), {'x': 5})  # 딕셔너리로 출력
    
    print(f"{a, b, args, kwargs['x']}")
    >> (1, 2, (3, 4), 5)  # 키값을 호출
    
    print(f"{a, b, args, kwargs.get('x')}")
    >> (1, 2, (3, 4), 5)  # get으로도 키값을 호출이 가능하다
    
    return

numbers(1,2,3,4,x=5)
```
### 딕셔너리형 변수 예시
```py
def numbers(a, b, **kwargs):
	print(f"{a, b, kwargs}")
    >> (1, 2, {'x': 3, 'y': 4})
    
    return
    
dict = {
    'x':3,
    'y':4
    }

numbers(1,2,**dict)
# 이미 딕셔너리화 되어있는 변수에 **를 붙여서 전달할 수 있다
```
<br>

## 2. mutable, immutable 특성과 자료형 종류
변수의 종류에는 mutable과 immutable 이 있다

mutable : 값이 변할 수 있다, 변수들은 각자의 객체값을 가리키므로 메모리가 유동적이다
- 리스트, 딕셔너리 자료형

immutable : 값이 변할 수 없다, 변수들은 모두 하나의 객체값을 가리키므로 메모리가 고정적이다
- 문자, 숫자, boolean, 튜플 자료형
<br>

## 3. 모델 필드의 종류
공식 문서  https://docs.djangoproject.com/en/4.0/ref/models/fields/#django.db.models.TextField

### 🔸문자열
* CharField(max_length=None) : 짧은 문자열
* EmailField(max_length=None) : 이메일형식
* TextField() : 긴 문자열에 사용
> max_length : 허용되는 최대 글자 수, 적당한 길이를 지정해주는 것이 용량 소모가 적다

### 🔸날짜/시간
* DateTimeField(auto_now_add=False, auto_now=False)
* DateField(auto_now_add=False, auto_now=False)
* TimeField(auto_now_add=False, auto_now=False)
> auto_now_add : DB가 생성될 때의 시간을 기준
>
> auto_now : DB가 수정될 때마다의 시간을 기준

### 🔸숫자
* IntegerField() : 정수
* FloatField() : 실수
* DecimalField(max_digits=None, decimal_places=None) : 실수
> max_digits : 허용되는 최대 자릿수, decimal_places 보다 같거나 커야한다
> 
> decimal_places : DB에 저장할 최대 자릿수

### 🔸다른 테이블과 연관을 지어 줄 때
* ForeignKey(to, on_delete=models.**OPTION**)
> to : 연관되는 모델명
> 
> on_delete=models.option : 연결된 데이터가 삭제되었을때 어떻게 처리할 것인지 지정해야한다
```py
# ForeignKey OPTION 종류
CASCADE : 연결되어있던 데이터를 삭제한다
PROTECT : 삭제시키지 않는다 (권장되지 않음)
SET_NULL : 데이터를 NULL로 바꾼다 (null=True 옵션도 추가해주어야함)
SET_DEFAULT : default 값으로 바꾼다 (default 값이 있을때에만 가능)
SET() : SET에 설정된 함수 등에 의해 바꾼다
DO_NOTHING : 아무런 행동을 취하지 않는다 (참조 무결성을 해칠 위험이 있어 권장되지 않음)
```
<br>

* ManyToManyField(to) : 다대다 관계에서 사용하며 해당 모델 db가 아닌 다른 해당 필드 전용 db에 생성되고 거기서 관리됨
> to : 연결된 모델명
> 
> related.name : 역참조 이름 지정 가능

###  Unique 옵션
아이디처럼 중복값이 허용되지 않는 경우 옵션에 unique=True 를 주어서 중복값을 제한할 수 있다
<br>

## 4. queryset, object 차이점
장고에서 .get('key':value)로 데이터를 가져오면 object 형식으로 가져오고,
.filter('key':value)는 queryset 형식으로 가져온다

둘의 차이점으로는 만약 get 할때 해당 데이터가 없다면 에러가 나지만, queryset은 데이터가 존재하지않더라도 빈리스트로 가져와서 정상적으로 작동이 된다

때문에 .get 은 try 예외처리를 함께 작성해주어야 데이터가 존재하지않을때의 에러를 방지할 수 있다

.filter는 빈리스트를 가져오는 경우를 따로 처리해줌으로써 기능을 보완할 수 있다
