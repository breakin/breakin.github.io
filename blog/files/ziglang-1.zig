// Build using 'zig build-exe ziglang-1.zig'

const std = @import("std");

pub const MaterialStateTexture = struct {
    texture_id: c_uint = 0
};

pub const PBRMaterialState = struct {
    albedo_texture: MaterialStateTexture = MaterialStateTexture {},
    emissive_texture: MaterialStateTexture = MaterialStateTexture {},
    roughness: f32 = 0.0,
    pub fn calculate_hash(self: PBRMaterialState) u32 {
        const hasher = std.hash.Murmur2_32;
        var hv : u32 = 0;
        const t = @typeInfo(PBRMaterialState);
        inline for (t.Struct.fields) |value| {
            if (value.field_type == MaterialStateTexture) {
                hv = hasher.hashUint32WithSeed(@field(self, value.name).texture_id, hv);
            }
        }
        return hv;
    }
};

pub fn hash_test() void {
    const ms = PBRMaterialState {};
    const hash_value = ms.calculate_hash();
    std.debug.print("Hash value was {}\n", .{hash_value});
}

pub const TestStruct = struct {
    a: i32 = 0,
    b: i32 = 0
};

pub fn debug_test() void {
    var t = TestStruct {};
    t.a = 99;
    t.b = 484;
    var c : i32 = t.a + t.b;
    std.debug.print("Hello {} {} {}\n", .{t.a,t.b,c});
}

pub fn main() void {
    hash_test();
    debug_test();
}