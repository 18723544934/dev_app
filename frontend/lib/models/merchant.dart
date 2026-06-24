class Merchant {
  final String id;
  final String name;
  final String? coverImage;
  final double rating;
  final int reviewCount;
  final int avgPrice;
  final int distance;
  final String address;
  final int businessStatus;
  final List<String> tags;

  Merchant({
    required this.id,
    required this.name,
    this.coverImage,
    this.rating = 0.0,
    this.reviewCount = 0,
    this.avgPrice = 0,
    this.distance = 0,
    this.address = '',
    this.businessStatus = 1,
    this.tags = const [],
  });

  factory Merchant.fromJson(Map<String, dynamic> json) {
    return Merchant(
      id: json['id']?.toString() ?? '',
      name: json['name'] ?? '',
      coverImage: json['cover_image'],
      rating: (json['rating'] ?? 0).toDouble(),
      reviewCount: json['review_count'] ?? 0,
      avgPrice: json['avg_price'] ?? 0,
      distance: json['distance'] ?? 0,
      address: json['address'] ?? '',
      businessStatus: json['business_status'] ?? 1,
      tags: (json['tags'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
    );
  }

  bool get isOpen => businessStatus == 1;

  String get distanceText {
    if (distance < 1000) {
      return '${distance}m';
    }
    return '${(distance / 1000).toStringAsFixed(1)}km';
  }
}
