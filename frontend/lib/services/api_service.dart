import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/category.dart';
import '../models/merchant.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api/v1';

  // 获取所有分类
  Future<List<Category>> getCategories() async {
    final response = await http.get(Uri.parse('$baseUrl/categories'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['code'] == 0 && data['data'] != null) {
        return (data['data']['list'] as List)
            .map((json) => Category.fromJson(json))
            .toList();
      }
    }
    throw Exception('获取分类失败');
  }

  // 随机抽取
  Future<Map<String, dynamic>> drawCategory({
    required int userId,
    bool includeCustom = true,
    List<int> categoryIds = const [],
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/draw'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'user_id': userId,
        'include_custom': includeCustom,
        'category_ids': categoryIds,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['code'] == 0) {
        return data['data'];
      }
    }
    throw Exception('抽取失败');
  }

  // 获取抽取历史
  Future<List<Map<String, dynamic>>> getDrawHistory(int userId, {int limit = 10}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/draw/history/$userId?limit=$limit'),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['code'] == 0 && data['data'] != null) {
        return (data['data']['list'] as List).cast<Map<String, dynamic>>();
      }
    }
    return [];
  }

  // 获取商家列表
  Future<Map<String, dynamic>> getMerchants({
    required int categoryId,
    required double longitude,
    required double latitude,
    String sortType = 'distance',
    int page = 1,
    int pageSize = 20,
    int radius = 3000,
  }) async {
    final response = await http.get(Uri.parse(
      '$baseUrl/merchants/list?category_id=$categoryId&'
      'longitude=$longitude&latitude=$latitude&'
      'sort_type=$sortType&page=$page&page_size=$pageSize&radius=$radius',
    ));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['code'] == 0) {
        return data['data'];
      }
    }
    throw Exception('获取商家列表失败');
  }

  // 获取商家详情
  Future<Merchant> getMerchantDetail(String merchantId) async {
    final response = await http.get(Uri.parse('$baseUrl/merchants/$merchantId'));

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      if (data['code'] == 0) {
        return Merchant.fromJson(data['data']);
      }
    }
    throw Exception('获取商家详情失败');
  }
}
