class Category {
  final int id;
  final String name;
  final int parentId;
  final String? keyword;
  final String? icon;
  final int sort;
  final bool isDefault;

  Category({
    required this.id,
    required this.name,
    this.parentId = 0,
    this.keyword,
    this.icon,
    this.sort = 0,
    this.isDefault = true,
  });

  factory Category.fromJson(Map<String, dynamic> json) {
    return Category(
      id: json['id'],
      name: json['name'],
      parentId: json['parent_id'] ?? 0,
      keyword: json['keyword'],
      icon: json['icon'],
      sort: json['sort'] ?? 0,
      isDefault: json['is_default'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'parent_id': parentId,
      'keyword': keyword,
      'icon': icon,
      'sort': sort,
      'is_default': isDefault,
    };
  }
}
