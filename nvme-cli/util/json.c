// SPDX-License-Identifier: GPL-2.0-or-later
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <errno.h>
#include <stdarg.h>
#include "json.h"

static inline void fail_and_notify(void)
{
	fprintf(stderr, "Allocation of memory for json object failed, aborting.\n");
	abort();
}

struct json_object *json_create_object(void)
{
	void *test = calloc(1, sizeof(struct json_object));
	if (!test)
		fail_and_notify();
	return test;
}

struct json_object *json_create_array(void)
{
	void *test = calloc(1, sizeof(struct json_object));
	if (!test)
		fail_and_notify();
	return test;
}

static struct json_pair *json_create_pair(const char *name, struct json_value *value)
{
	struct json_pair *pair = malloc(sizeof(struct json_pair));
	if (pair) {
		pair->name = strdup(name);
		pair->value = value;

		value->parent_type = JSON_PARENT_TYPE_PAIR;
		value->parent_pair = pair;
	} else
		fail_and_notify();

	return pair;
}

static struct json_value *json_create_value_int(long long number)
{
	struct json_value *value = malloc(sizeof(struct json_value));

	if (value) {
		value->type = JSON_TYPE_INTEGER;
		value->integer_number = number;
	} else
		fail_and_notify();

	return value;
}

static struct json_value *json_create_value_uint(unsigned long long number)
{
	struct json_value *value = malloc(sizeof(struct json_value));

	if (value) {
		value->type = JSON_TYPE_UINT;
		value->uint_number = number;
	} else
		fail_and_notify();

	return value;
}

static struct json_value *json_create_value_float(long double number)
{
	struct json_value *value = malloc(sizeof(struct json_value));

	if (value) {
		value->type = JSON_TYPE_FLOAT;
		value->float_number = number;
	}  else
		fail_and_notify();

	return value;
}

static char *strdup_escape(const char *str)
{
	const char *input = str;
	char *p, *ret;
	int escapes;

	if (!strlen(str))
		return NULL;

	escapes = 0;
	while ((input = strpbrk(input, "\\\"")) != NULL) {
		escapes++;
		input++;
	}

	p = ret = malloc(strlen(str) + escapes + 1);
	if (!ret)
		fail_and_notify();

	while (*str) {
		if (*str == '\\' || *str == '\"')
			*p++ = '\\';
		*p++ = *str++;
	}
	*p = '\0';

	return ret;
}

/*
 * Valid JSON strings must escape '"' and '/' with a preceding '/'
 */
static struct json_value *json_create_value_string(const char *str)
{
	struct json_value *value = malloc(sizeof(struct json_value));

	if (value) {
		value->type = JSON_TYPE_STRING;
		value->string = strdup_escape(str ? str : "(null)");
		if (!value->string) {
			free(value);
			value = NULL;
			return value;
		}
	}
	if (!value)
		fail_and_notify();

	return value;
}

static struct json_value *json_create_value_object(struct json_object *obj)
{
	struct json_value *value = malloc(sizeof(struct json_value));

	if (value) {
		value->type = JSON_TYPE_OBJECT;
		value->object = obj;
		obj->parent = value;
	} else
		fail_and_notify();

	return value;
}

static struct json_value *json_create_value_array(struct json_object *array)
{
	struct json_value *value = malloc(sizeof(struct json_value));

	if (value) {
		value->type = JSON_TYPE_ARRAY;
		value->array = array;
		array->parent = value;
	} else
		fail_and_notify();

	return value;
}

static void json_free_pair(struct json_pair *pair);
static void json_free_value(struct json_value *value);

void json_free_object(struct json_object *obj)
{
	int i;

	for (i = 0; i < obj->pair_cnt; i++)
		json_free_pair(obj->pairs[i]);
	free(obj->pairs);
	free(obj);
}

void json_free_array(struct json_object *array)
{
	int i;

	for (i = 0; i < array->value_cnt; i++)
		json_free_value(array->values[i]);
	free(array->values);
	free(array);
}

static void json_free_pair(struct json_pair *pair)
{
	json_free_value(pair->value);
	free(pair->name);
	free(pair);
}

static void json_free_value(struct json_value *value)
{
	switch (value->type) {
	case JSON_TYPE_STRING:
		free(value->string);
		break;
	case JSON_TYPE_OBJECT:
		json_free_object(value->object);
		break;
	case JSON_TYPE_ARRAY:
		json_free_array(value->array);
		break;
	}
	free(value);
}

static int json_array_add_value(struct json_object *array, struct json_value *value)
{
	struct json_value **values = realloc(array->values,
		sizeof(struct json_value *) * (array->value_cnt + 1));

	if (!values)
		return ENOMEM;
	values[array->value_cnt] = value;
	array->value_cnt++;
	array->values = values;

	value->parent_type = JSON_PARENT_TYPE_ARRAY;
	value->parent_array = array;
	return 0;
}

static int json_object_add_pair(struct json_object *obj, struct json_pair *pair)
{
	struct json_pair **pairs = realloc(obj->pairs,
		sizeof(struct json_pair *) * (obj->pair_cnt + 1));
	if (!pairs)
		return ENOMEM;
	pairs[obj->pair_cnt] = pair;
	obj->pair_cnt++;
	obj->pairs = pairs;

	pair->parent = obj;
	return 0;
}

int json_object_add_value_type(struct json_object *obj, const char *name, int type, ...)
{
	struct json_value *value;
	struct json_pair *pair;
	va_list args;
	int ret;

	va_start(args, type);
	if (type == JSON_TYPE_STRING)
		value = json_create_value_string(va_arg(args, char *));
	else if (type == JSON_TYPE_INTEGER)
		value = json_create_value_int(va_arg(args, long long));
	else if (type == JSON_TYPE_UINT)
		value = json_create_value_uint(va_arg(args, unsigned long long));
	else if (type == JSON_TYPE_FLOAT)
		value = json_create_value_float(va_arg(args, long double));
	else if (type == JSON_TYPE_OBJECT)
		value = json_create_value_object(va_arg(args, struct json_object *));
	else
		value = json_create_value_array(va_arg(args, struct json_object *));
	va_end(args);

	if (!value)
		return ENOMEM;

	pair = json_create_pair(name, value);
	if (!pair) {
		json_free_value(value);
		return ENOMEM;
	}
	ret = json_object_add_pair(obj, pair);
	if (ret) {
		json_free_pair(pair);
		return ENOMEM;
	}
	return 0;
}

static void json_print_array(struct json_object *array, void *);
int json_array_add_value_type(struct json_object *array, int type, ...)
{
	struct json_value *value;
	va_list args;
	int ret;

	va_start(args, type);
	if (type == JSON_TYPE_STRING)
		value = json_create_value_string(va_arg(args, char *));
	else if (type == JSON_TYPE_INTEGER)
		value = json_create_value_int(va_arg(args, long long));
	else if (type == JSON_TYPE_UINT)
		value = json_create_value_uint(va_arg(args, unsigned long long));
	else if (type == JSON_TYPE_FLOAT)
		value = json_create_value_float(va_arg(args, double));
	else if (type == JSON_TYPE_OBJECT)
		value = json_create_value_object(va_arg(args, struct json_object *));
	else
		value = json_create_value_array(va_arg(args, struct json_object *));
	va_end(args);

	if (!value)
		return ENOMEM;

	ret = json_array_add_value(array, value);
	if (ret) {
		json_free_value(value);
		return ENOMEM;
	}
	return 0;
}

static int json_value_level(struct json_value *value);
static int json_pair_level(struct json_pair *pair);
static int json_array_level(struct json_object *array);
static int json_object_level(struct json_object *object)
{
	if (object->parent == NULL)
		return 0;
	return json_value_level(object->parent);
}

static int json_pair_level(struct json_pair *pair)
{
	return json_object_level(pair->parent) + 1;
}

static int json_array_level(struct json_object *array)
{
	return json_value_level(array->parent);
}

static int json_value_level(struct json_value *value)
{
	if (value->parent_type == JSON_PARENT_TYPE_PAIR)
		return json_pair_level(value->parent_pair);
	else
		return json_array_level(value->parent_array) + 1;
}

static void json_print_level(int level, void *out)
{
	while (level-- > 0)
		printf("  ");
}

static void json_print_pair(struct json_pair *pair, void *);
static void json_print_array(struct json_object *array, void *);
static void json_print_value(struct json_value *value, void *);
void json_print_object(struct json_object *obj, void *out)
{
	int i;

	printf("{\n");
	for (i = 0; i < obj->pair_cnt; i++) {
		if (i > 0)
			printf(",\n");
		json_print_pair(obj->pairs[i], out);
	}
	printf("\n");
	json_print_level(json_object_level(obj), out);
	printf("}");
}

static void json_print_pair(struct json_pair *pair, void *out)
{
	json_print_level(json_pair_level(pair), out);
	printf("\"%s\" : ", pair->name);
	json_print_value(pair->value, out);
}

static void json_print_array(struct json_object *array, void *out)
{
	int i;

	printf("[\n");
	for (i = 0; i < array->value_cnt; i++) {
		if (i > 0)
			printf(",\n");
		json_print_level(json_value_level(array->values[i]), out);
		json_print_value(array->values[i], out);
	}
	printf("\n");
	json_print_level(json_array_level(array), out);
	printf("]");
}

static void json_print_value(struct json_value *value, void *out)
{
	switch (value->type) {
	case JSON_TYPE_STRING:
		printf( "\"%s\"", value->string);
		break;
	case JSON_TYPE_INTEGER:
		printf( "%lld", value->integer_number);
		break;
	case JSON_TYPE_UINT:
		printf( "%llu", value->uint_number);
		break;
	case JSON_TYPE_FLOAT:
		printf( "%.0Lf", value->float_number);
		break;
	case JSON_TYPE_OBJECT:
		json_print_object(value->object, out);
		break;
	case JSON_TYPE_ARRAY:
		json_print_array(value->array, out);
		break;
	}
}
